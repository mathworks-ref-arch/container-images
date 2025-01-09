#!/bin/sh

# Copyright 2022-2024 The MathWorks, Inc.

set -e

#=======================================================================
build_cmd() { # Takes the cmd input string and outputs the same
    # string correctly quoted to be evaluated again.
    #
    # Always returns a 0
    #
    # usage: build_cmd
    #

    # Use version of echo here that will preserve
    # backslashes within $cmd.

    echo "$1" | awk '
#----------------------------------------------------------------------------
        BEGIN { squote = sprintf ("%c", 39)   # set single quote
                dquote = sprintf ("%c", 34)   # set double quote
              }
          NF != 0 { newarg=dquote             # initialize output string to
                                              # double quote
          lookquote=dquote                    # look for double quote
          oldarg = $0
          while ((i = index (oldarg, lookquote))) {
             newarg = newarg substr (oldarg, 1, i - 1) lookquote
             oldarg = substr (oldarg, i, length (oldarg) - i + 1)
             if (lookquote == dquote)
                lookquote = squote
             else
                lookquote = dquote
             newarg = newarg lookquote
          }
          printf " %s", newarg oldarg lookquote }
#----------------------------------------------------------------------------
        '
    return 0
}

exportInBashrc() {
    # There are some environment variables that we want to ensure are available
    # in all bash sessions (for example a session started with `docker exec`) that
    # might not inherit from this process. To ensure these exist we write them
    # into ~/.bashrc so that any bash session started acquires them correctly.
    while [ $# -gt 0 ]; do
        KEY=$1
        eval "VALUE=\$$KEY"
        echo "export $KEY=$VALUE" >>~/.bashrc
        shift
    done
}

getMATLABVersion() {
    stat /usr/local/bin/matlab | grep -Eo "R[0-9]{4}[ab]"
}

printMessage() {
    # Print README file according to the mode in which the container is running.
    echo ----------------------------------------------------
    cat "/etc/$1"
    echo ----------------------------------------------------
}

startVNCServer() {
    # Clean up VNC lock files in case they still exist - note that this is also important
    # when we undertake a `docker stop` / `docker restart` workflow, since the entrypoint is
    # run a second time and the temp .X files will exist. This code also allows for an
    # install into a running container / docker commit workflow to expand the capabilities
    # of this container.
    sudo rm -rf /tmp/.X*

    /usr/bin/vncserver -localhost no >/dev/null 2>&1
    /opt/noVNC/utils/launch.sh --vnc localhost:5901 >/dev/null 2>&1 &
}

validateInput() {
    # Validate the flags the user provided.

    if [ "${modes}" -gt 1 ]; then
        printf "Error: -help, -vnc, -shell and -browser are mutually exclusive.\n"
        printf "Use the -help option to review the API documentation for this container.\n"
        exit 1
    fi
}

checkLicensing() {
    # Check for the existence of a MATLAB licensing environment variable
    if [ -n "${MLM_LICENSE_FILE}" ]; then
        # if it is present then lets assume we are trying to run on-prem.
        export USAGE=onprem
    else
        export USAGE=cloud
    fi

    exportInBashrc USAGE

    # Check for the format of the license file variable.
    # If the format is port@hostname, export it. Otherwise, assume the user has mounted a folder and copy the specified file to the right place.
    if [ -n "${MLM_LICENSE_FILE}" ]; then
        if echo "${MLM_LICENSE_FILE}" | grep -qEo "[0-9]+@.+"; then
            exportInBashrc MLM_LICENSE_FILE
            LICENSE_MESSAGE="Licensing MATLAB using the license manager $MLM_LICENSE_FILE."
        else
            # Check that file exists otherwise exit immediately.
            if [ ! -f "${MLM_LICENSE_FILE}" ]; then
                printf "The license file specified does not exist.\n"
                exit
            fi
            LICENSE_MESSAGE="Licensing MATLAB using license file $MLM_LICENSE_FILE."
        fi
    else
        # Append licmode to the arglist
        ARGLIST="-licmode online ${ARGLIST}"
    fi

    # Alias `matlab` to append ARGLIST to implement the startup logic. This allows the automatic
    # inclusion of MATLAB configuration such as licensing arguments. For example:
    # `matlab -licmode online`
    echo "alias matlab=\"matlab ${ARGLIST}\"" >>~/.bashrc
}

checkSharedMemorySpace() {
    # Only print the warning if a display will be used
    if [ "${VNC}" = true ] || [ "${SHELL}" = true ] || [ "${BROWSER}" = true ]; then

        # Find the size of your shared memory space by calling df on the /dev/shm directory
        # Take the second line of output (the size) and extract the numeric value.
        SHM_SIZE=$(df /dev/shm --output=size | sed -n '2p' | grep -oE "[0-9]+")

        if [ -n "${SHM_SIZE}" ]; then
            # Check it is big enough
            if [ "${SHM_SIZE}" -le 524200 ]; then
                echo
                echo "WARNING:"
                echo
                echo "This container has a shared area (/dev/shm) of size ${SHM_SIZE}kB. The MATLAB"
                echo "desktop requires at least 512MB to run correctly. Restart the container with"
                echo " --shm-size=512M in the docker command line."
                echo
            fi
        fi
    fi
}

checkEnvironmentVariables() {
    # If there is an environment variable called PASSWORD (expected to be set on the
    # command line of docker) then use it to set the VNC password
    if [ -n "${PASSWORD}" ]; then
        if [ "$(echo "${PASSWORD}" | grep -Eo '.{6,}')" ]; then
            printf "%s\n%s\n\n" "${PASSWORD}" "${PASSWORD}" | vncpasswd >/dev/null 2>&1
            touch "$HOME/.Xresources" &
        else
            printf "Error: the password should be at least 6 characters.\n"
            exit 1
        fi
    else
        # Assume default password so make browser VNC auto connect
        sudo rm /opt/noVNC/index.html
        sudo ln -s /opt/noVNC/redirect.html /opt/noVNC/index.html
    fi

    # Test and expand up proxy settings for MathWorks Service Host and MATLAB itself.
    if [ -n "${PROXY_SETTINGS}" ]; then

        # The input PROXY_SETTINGS could be a string of ANY of the following forms:
        #   1) proxy.fqdn.com:12345
        #   2) http://proxy.fqdn.com:12345
        #   3) http://user:pass@proxy.fqdn.com:12345
        #
        # In each case the field separator is considered to be either : OR @ and we search based on that criteria.
        # Case 1 (with NF == 2) finds all instances of the first case.
        # Case 2 (with NF == 3) finds the second case (and more) and removes the // from the hostname before setting
        # Case 3 (with NF == 5) finds the third case (and more)
        eval "$(
            echo "${PROXY_SETTINGS}" | awk -F'[:@/]' '
            #----------------------------------------------------------------------------
            (NF == 1) { exit 1 }
            (NF == 2) { http_spec="http://"$0; host=$1; port=$2 }
            (NF > 2 && $1 ~ /^http$/ ) { http_spec=$0; }
            (NF >= 5 && http_spec ) {host=$4; port=$5}
            (NF >= 7 && http_spec ) {user=$4; pass=$5; host=$6; port=$7}
            {printf "export no_proxy=localhost "}
            (host ~ /^[A-Za-z0-9_\-\.]+$/ && port ~ /^[0-9]+$/) {printf "http_proxy=%s https_proxy=%s MW_PROXY_HOST=%s MW_PROXY_PORT=%s ", http_spec, http_spec, host, port}
            (user && pass) { printf "MW_PROXY_USERNAME=%s MW_PROXY_PASSWORD=%s", user, pass }
            {printf "\n"}
            #----------------------------------------------------------------------------
            '
        )"

        if [ $? -ne 0 ]; then
            echo
            echo "WARNING:"
            echo
            echo "Invalid PROXY_SETTINGS setting: ${PROXY_SETTINGS}"
            echo "The correct form is proxy-hostname:proxy-port where proxy-hostname"
            echo "can be a short hostname, a fully qualified hostname or an IP address"
            echo
        else
            export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS} -Dtmw.proxyHost.override=${MW_PROXY_HOST} -Dtmw.proxyPort.override=${MW_PROXY_PORT}"
            if [ -n "${MW_PROXY_USERNAME}" ]; then
                export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS} -Dtmw.proxyUser.override=${MW_PROXY_USERNAME} -Dtmw.proxyPassword.override=${MW_PROXY_PASSWORD}"
            fi
            exportInBashrc no_proxy http_proxy https_proxy MW_PROXY_HOST MW_PROXY_PORT MW_PROXY_USERNAME MW_PROXY_PASSWORD
        fi
    fi
}

startContainer() {

    # In help mode, just print the help message
    if [ "${HELP}" = true ]; then

        printMessage help_readme

    # In desktop mode, print vnc message and start the VNC server in the background
    elif [ "${VNC}" = true ] || [ "${SHELL}" = true ]; then

        printMessage vnc_readme
        startVNCServer

        # Always want everything to start in the user home folder
        cd ~/Documents/MATLAB/ || exit 1
        exec bash

    # In browser mode, print the web message and start matlab-proxy
    elif [ "${BROWSER}" = true ]; then

        printMessage browser_readme
        eval exec "matlab-proxy-app ${CUSTOM_COMMAND}"

    # Otherwise, run MATLAB
    else

        if [ -z "${LICENCE_MESSAGE}" ]; then
            echo "${LICENSE_MESSAGE}"
        fi

        cd ~/Documents/MATLAB/ || exit 1
        eval exec "matlab ${ARGLIST} ${CUSTOM_COMMAND}"
    fi
}
