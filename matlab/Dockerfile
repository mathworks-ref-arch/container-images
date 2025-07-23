# Copyright 2024-2025 The MathWorks, Inc.

# This Dockerfile allows you to build either the MATLAB Container image or the MATLAB Deep Learning Container image.

# To specify which MATLAB release to install in the container, edit the value of the MATLAB_RELEASE argument.
ARG MATLAB_RELEASE=""

# Specify the additional list of toolboxes and support packages to install into the
# mathworks/matlab-deep-learning Docker image.
ARG ADDITIONAL_PRODUCTS=""

# Specify any additional flags used to customise the `mpm` installation process.
ARG MPM_ADDITIONAL_FLAGS=""

# Specify the base repository to pull MATLAB dependencies from.
ARG MATLAB_DEPS_IMAGE=""

# Pin to a specific Ubuntu version to ensure images can be updated independently of defaults for matlab-deps.
# Should be a ubuntu-based image e.g. `ubuntu20.04`
# Leave blank to use the default OS
ARG MATLAB_DEPS_OS=""

# Specify the URL of the managed version of MathWorks Service Host.
ARG MATHWORKS_SERVICE_HOST_INSTALL_URL=""

ARG GCC=""
ARG GPP=""

# Specify MATLAB Install Location.
ARG MATLAB_INSTALL_LOCATION="/opt/matlab/${MATLAB_RELEASE}"

# When you start the build stage, this Dockerfile by default uses the Ubuntu-based matlab-deps image.
# To check the available matlab-deps images, see: https://hub.docker.com/r/mathworks/matlab-deps
FROM ${MATLAB_DEPS_IMAGE}:${MATLAB_RELEASE}${MATLAB_DEPS_OS:+-$MATLAB_DEPS_OS} AS build
ARG MATLAB_RELEASE
ARG MATLAB_INSTALL_LOCATION
ARG MPM_ADDITIONAL_FLAGS
ARG MATHWORKS_SERVICE_HOST_INSTALL_URL
ARG GCC
ARG GPP

# Install extra tools not included in `matlab-deps`.
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --yes --no-install-recommends \
    apt-utils \
    # Requirements for mpm
    ca-certificates \
    # Requirements for mex generation
    ${GCC} \
    ${GPP} \
    # Requirements for VNC
    libglu1-mesa \
    libosmesa6 \
    xfce4 \
    xscreensaver \
    # Requirements for matlab-proxy and noVNC
    python3 \
    python3-pip \
    pipx \
    xvfb \
    # Utility Software
    tini \
    sudo \
    curl \
    wget \
    nano \
    xfce4-terminal \
    psmisc \
    less \
    && apt-get remove -y \
    tumbler \
    pulseaudio \
    gvfs \
    gnome-screensaver \
    && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# Set the gcc and g++ soft links
RUN ln -s $(which ${GCC}) /usr/bin/gcc && \
    ln -s $(which ${GPP}) /usr/bin/g++

################################################################################
# Setup VNC
################################################################################

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --yes --no-install-recommends \
    tigervnc-standalone-server \
    tigervnc-common \
    dbus-x11 \
    tigervnc-tools \
    && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

ARG NOVNC=/opt/noVNC

# Clone noVNC and websockify.
RUN mkdir -p ${NOVNC}/utils/websockify \
    && curl -sSfL 'https://github.com/novnc/noVNC/archive/v1.2.0.tar.gz' | sudo tar -zxf - -C ${NOVNC} --strip=1 \
    && curl -sSfL 'https://github.com/novnc/websockify/archive/v0.10.0.tar.gz' | sudo tar -zxf - -C ${NOVNC}/utils/websockify --strip=1 \
    && find ${NOVNC} -name ".git*" | sudo xargs rm -rf \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s $NOVNC/vnc.html $NOVNC/index.html

EXPOSE 5901 6080

################################################################################
# Add predefined configuration
################################################################################

COPY build/config/localsudo       /etc/sudoers.d/
COPY build/run.sh                 /bin/run.sh
COPY build/utils.sh               /bin/utils.sh
COPY build/readmes/welcome_readme /etc/welcome_readme
COPY build/readmes/help_readme    /etc/help_readme
COPY build/readmes/vnc_readme     /etc/vnc_readme
COPY build/readmes/browser_readme /etc/browser_readme

# Set up the README files to show the correct MATLAB release
RUN for file in $(ls /etc/*_readme); do \
    sed -i "s/{{MATLAB_RELEASE}}/${MATLAB_RELEASE}/g" "${file}"; \
    done

################################################################################
# Setup matlab user
################################################################################

ARG HOME=/home/matlab

# Add "matlab" user, grant sudo permission and set default VNC password to "matlab".
RUN adduser --home ${HOME} --shell /bin/bash --disabled-password --gecos "" matlab \
    && echo "matlab ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/matlab \
    && chmod 0440 /etc/sudoers.d/matlab

# Set user and work directory.
USER matlab
WORKDIR /home/matlab

################################################################################
# Install MATLAB
################################################################################

# Run mpm to install MATLAB in the target location and delete the mpm installation afterwards.
# If mpm fails to install successfully, then print the logfile in the terminal, otherwise clean up.
# Remove the pre packaged libstdc libraries to force MATLAB to use the system libraries.
RUN wget -q https://www.mathworks.com/mpm/glnxa64/mpm \
    && chmod +x mpm \
    && sudo HOME=${HOME} ./mpm install \
    --release=${MATLAB_RELEASE} \
    --destination=${MATLAB_INSTALL_LOCATION} \
    ${MPM_ADDITIONAL_FLAGS} \
    --products "MATLAB" \
    || (echo "MPM Installation Failure. See below for more information:" && cat /tmp/mathworks_root.log && false) \
    && sudo rm -f ${MATLAB_INSTALL_LOCATION}/sys/os/glnxa64/libstdc++.* \
    && sudo rm -f mpm /tmp/mathworks_root.log \
    && sudo ln -s ${MATLAB_INSTALL_LOCATION}/bin/matlab /usr/local/bin/matlab


################################################################################
# Setup MathWorks Service Host
################################################################################

ENV MW_SERVICEHOST_USE_HOSTNAME_FOR_PERSISTENCE="false"

ARG MSH_TMP="/tmp/install_managed_msh.sh"
ARG MSH_ROOT="/opt/MathWorks/ServiceHost"

RUN wget -O "${MSH_TMP}" "${MATHWORKS_SERVICE_HOST_INSTALL_URL}" \
    && chmod +x "${MSH_TMP}" \
    && sudo ${MSH_TMP} --destination ${MSH_ROOT} \
    && rm "${MSH_TMP}"

################################################################################
# Setup matlab-proxy
################################################################################

RUN mkdir -p ${HOME}/Documents/MATLAB/Add-Ons \
    && touch ${HOME}/Documents/MATLAB/Add-Ons/.toolboxFolders \
    && touch ${HOME}/Documents/MATLAB/Add-Ons/.zipFolders \
    && python3 -m pipx install matlab-proxy

ENV PATH=${HOME}/.local/bin:${PATH}

# These lines disable token authentication for container workflows by default.
# To re-enable, unset this environment variable.
ENV MWI_ENABLE_TOKEN_AUTH="False"

ENV MWI_APP_PORT=8888
EXPOSE ${MWI_APP_PORT}

################################################################################
# Setup user experience data collection
################################################################################

# The following environment variable allows MathWorks to understand how this MathWorks
# product (MATLAB Dockerfile) is being used. This information helps us make MATLAB even better.
# Your content, and information about the content within your files, is not shared with MathWorks.
# To opt out of this service, unset the environment variables defined in the following line.
# To learn more, see the Help Make MATLAB Even Better section in the accompanying README:
# https://github.com/mathworks-ref-arch/matlab-dockerfile#help-make-matlab-even-better
ENV MW_DDUX_FORCE_ENABLE=true

################################################################################
# Final Setup
################################################################################

# Setup the container's desktop environment.
COPY build/config/xstartup       ${HOME}/.vnc/
COPY build/config/MATLAB.desktop ${HOME}/Desktop/
COPY build/config/xfce4/         ${HOME}/.config/xfce4/
COPY build/config/startup.m      ${HOME}/Documents/MATLAB/

# Make sure that MATLAB is running Windows shortcuts.
COPY build/config/matlab.prf     ${HOME}/.matlab/${MATLAB_RELEASE}/

# By adding this configuration file we turn off the screensaver for the VNC session by default.
COPY build/config/xscreensaver   ${HOME}/.xscreensaver

RUN sudo chown -R matlab:matlab ${HOME} \
    && chmod +x  ${HOME}/.vnc/xstartup \
    && chmod u+w ${HOME}/Desktop/MATLAB.desktop \
    && chmod u+w ${HOME}/.matlab/${MATLAB_RELEASE}/matlab.prf \
    && chmod +x  ${HOME}/Desktop/MATLAB.desktop \
    && touch     ${HOME}/.Xauthority \
    && sed -i "s/{{MATLAB_RELEASE}}/${MATLAB_RELEASE}/g" ${HOME}/Desktop/MATLAB.desktop

COPY build/config/novnc_login_redirect.html ${NOVNC}/redirect.html


ARG DEFAULT_VNC_PASSWORD=matlab

RUN printf "${DEFAULT_VNC_PASSWORD}\n${DEFAULT_VNC_PASSWORD}\n\n" | vncpasswd

WORKDIR /home/matlab/Documents/MATLAB/
ENTRYPOINT ["tini", "--", "/bin/run.sh"]
CMD []

################################################################################
# Build target for the mathworks/matlab-deep-learning image
################################################################################

FROM build AS matlab-deep-learning

ARG MATLAB_RELEASE
ARG MATLAB_INSTALL_LOCATION
ARG ADDITIONAL_PRODUCTS
ARG MPM_ADDITIONAL_FLAGS

# Run mpm to install MATLAB in the target location and delete the mpm installation afterwards.
# If mpm fails to install successfully, then print the logfile in the terminal, otherwise clean up.
# Pass in $HOME variable to install support packages into the user's HOME folder.
# Remove the pre packaged libstdc libraries to force MATLAB to use the system libraries.
RUN wget -q https://www.mathworks.com/mpm/glnxa64/mpm \
    && chmod +x mpm \
    && sudo HOME=${HOME} ./mpm install \
    --release=${MATLAB_RELEASE} \
    --destination=${MATLAB_INSTALL_LOCATION} \
    ${MPM_ADDITIONAL_FLAGS} \
    --products ${ADDITIONAL_PRODUCTS} \
    || (echo "MPM Installation Failure. See below for more information:" && cat /tmp/mathworks_root.log && false) \
    && sudo rm -f ${MATLAB_INSTALL_LOCATION}/sys/os/glnxa64/libstdc++.* \
    && sudo rm -rf mpm /tmp/mathworks_root.log

COPY build/config/matlab_deep_learning/MNISTExample.mlx ${HOME}/Documents/MATLAB/

# Set DDUX variables.
ENV MW_CONTEXT_TAGS=MATLAB:DEEPLEARNING:DOCKERHUB:V1
ENV MHLM_CONTEXT=MATLAB_DL_DOCKERHUB

################################################################################
# Build target for the mathworks/matlab image
################################################################################

FROM build AS matlab

# Set DDUX variables.
ENV MW_CONTEXT_TAGS=MATLAB:DOCKERHUB:V1
ENV MHLM_CONTEXT=MATLAB_DOCKERHUB
