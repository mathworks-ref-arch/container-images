#!/usr/bin/env bash

# Copyright 2021-2026 The MathWorks, Inc.

set -eu -o pipefail

run_setup_session() {
  local user=$1
  shift
  local user_home=$(getent passwd "$user" | cut -d: -f6)

  HOME="$user_home" sudo --preserve-env --user "$user" \
    script --quiet --command \
    "/bin/setup_session.sh $(printf '%q ' "$@")" /dev/null
}

modify_default_user() {
  local default_user_name="matlab"
  local target_name="${USER_NAME:-${default_user_name}}"
  local target_uid="${USER_UID:-}"
  local target_gid="${USER_GID:-}"
  
  unset USER_NAME USER_UID USER_GID

  local customisation_requested=false
  if [ "${target_name}" != "${default_user_name}" ] || [ -n "${target_uid}" ] || [ -n "${target_gid}" ]; then
    customisation_requested=true
  fi

  # If not root and customisation requested, error
  # Running as root is required to perform the modification without changing the user executing the script
  if [ "$(id -u)" -ne 0 ] && [ "${customisation_requested}" = true ]; then
    echo "Error: User customisation requires root. Run with '--user root'" >&2
    exit 1
  fi

  # If not root and not the default user, error
  local default_user_user=$(whoami)
  if [ "$(id -u)" -ne 0 ] && [ "${default_user_user}" != "${default_user_name}" ]; then
    echo "Error: Running as user '${default_user_user}' is not supported." >&2
    echo "Either run without '--user' or use '--user root' with USER_UID, USER_GID, or USER_NAME to customise the user." >&2
    exit 1
  fi

  # If not root, run as default_user user (must be default user at this point)
  if [ "$(id -u)" -ne 0 ]; then
    run_setup_session "$(whoami)" "$@"
    exit $?
  fi

  # Root with no customisation
  if [ "${customisation_requested}" = false ]; then
    echo "Running as root" >&2
    run_setup_session "root" "$@"
    exit $?
  fi

  # Validate UID and GID are positive integers
  if [ -n "${target_uid}" ] && ! [[ "${target_uid}" =~ ^[0-9]+$ ]]; then
    echo "Error: USER_UID must be a positive integer." >&2
    exit 1
  fi
  if [ -n "${target_gid}" ] && ! [[ "${target_gid}" =~ ^[0-9]+$ ]]; then
    echo "Error: USER_GID must be a positive integer." >&2
    exit 1
  fi

  # Reject UID/GID of 0 - they should use --user root without customisation instead
  if [ "${target_uid}" = "0" ] || [ "${target_gid}" = "0" ]; then
    echo "Error: USER_UID=0 and USER_GID=0 are not supported. To run as root, use '--user root' without USER_UID, USER_GID, or USER_NAME." >&2
    exit 1
  fi

  # Validate username format (POSIX compliant: 1-32 chars, starts with letter/underscore, lowercase alphanumeric with underscore/hyphen)
  if ! [[ "${target_name}" =~ ^[a-z_][a-z0-9_-]{0,31}$ ]]; then
    echo "Error: USER_NAME must be 1-32 characters, start with a letter or underscore, and contain only lowercase letters, digits, underscores, or hyphens." >&2
    exit 1
  fi

  # Root with customisation - modify default user
  local default_user_uid=$(id -u "${default_user_name}")
  local default_user_gid=$(id -g "${default_user_name}")
  local home="/home/${default_user_name}"

  # --- GID remapping ---
  # If the target GID (requested by the user) is different from the default GID, change the GID of the default user group
  # The target GID may already be claimed by a different group inside the image (e.g. a system group). 
  # groupmod refuses to assign a GID that is already in use, so we first bump the conflicting group out of the way by adding 10000 to its GID.
  # That offset is arbitrary but large enough to avoid collisions with anything meaningful, and the displaced group is never used directly by MATLAB or the user's session.
  if [ -n "${target_gid}" ] && [ "${target_gid}" != "${default_user_gid}" ]; then
    local existing_group=$(getent group "${target_gid}" | cut -d: -f1)
    if [ -n "${existing_group}" ]; then
      groupmod -g "$((target_gid + 10000))" "${existing_group}"
    fi
    # Reusing default_user_name as the default group name for convenience.
    groupmod -g "${target_gid}" "${default_user_name}"
  fi

  # --- UID remapping ---
  # Same pattern as GID: If the target UID (requested by the user) is different from the default UID, change the UID of the default user
  # The +10000 displaced user is effectively unreachable from a login perspective and exists only to keep /etc/passwd consistent (no orphaned UIDs).
  if [ -n "${target_uid}" ] && [ "${target_uid}" != "${default_user_uid}" ]; then
    local existing_user=$(getent passwd "${target_uid}" | cut -d: -f1)
    if [ -n "${existing_user}" ]; then
      usermod -u "$((target_uid + 10000))" "${existing_user}"
    fi
    usermod -u "${target_uid}" "${default_user_name}"
  fi

  # --- Username rename ---
  # If the target name (requested by the user) is different from the default name, rename the user name and the group name
  # Rename is done last, after UID/GID are already in place, so that all intermediate usermod/groupmod calls above still reference the known default name.
  # We reject the rename if the target name already exists to avoid silently merging two identities.
  # The sudoers drop-in file (which grants password-less sudo) must also be renamed and its contents updated, because sudo matches entries by the literal username string, not by UID.
  if [ "${target_name}" != "${default_user_name}" ]; then
    if getent passwd "${target_name}" >/dev/null 2>&1; then
      echo "Error: USER_NAME '${target_name}' conflicts with existing user" >&2
      exit 1
    fi
    usermod -l "${target_name}" "${default_user_name}"
    groupmod -n "${target_name}" "${default_user_name}"

    sed -i "s/${default_user_name}/${target_name}/g" "/etc/sudoers.d/${default_user_name}"
    mv "/etc/sudoers.d/${default_user_name}" "/etc/sudoers.d/${target_name}"
  fi

  # Fix ownership of the home directory so the (possibly remapped) UID:GID owns all files that were created under the original user at build time.
  # This is necessary because chown uses numeric IDs, so files previously owned by the old UID are now unowned from the kernel's perspective.
  chown -R "${target_name}:${target_name}" "${home}"

  # Update working directory to new user's home
  cd "${home}/Documents/MATLAB" 2>/dev/null || cd "${home}" || cd /

  run_setup_session "${target_name}" "$@"
}

modify_default_user "$@"
