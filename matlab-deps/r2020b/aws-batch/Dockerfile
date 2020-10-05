# Copyright 2020 The MathWorks, Inc.

FROM nvidia/cuda:11.0-base-ubuntu20.04

MAINTAINER MathWorks

# The following libraries are all required by MATLAB, except for:
# csh                  - Support MATLAB's Engine API for C and Fortran. See https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
# gcc, g++, gfortran   - Support Simulink code generation and mex with gcc, g++, or gfortran.
# locales, locales-all - Provide extended locales support
# python3, python3-pip - Python and pip are to run/install the AWS CLI.
# unzip, zip           - Used to stage input/output data.
RUN apt-get update && apt-get install --no-install-recommends -y \
    libasound2 \
    libatk1.0-0 \
    libc6 \
    libcairo-gobject2 \
    libcairo2 \
    libcrypt1 \
    libcups2 \
    libdbus-1-3 \
    libfontconfig1 \
    libgdk-pixbuf2.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpam0g \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libpython2.7 \
    libpython3.8 \
    libselinux1 \
    libsm6 \
    libsndfile1 \
    libtcl8.6 \
    libuuid1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxft2 \
    libxi6 \
    libxinerama1 \
    libxrandr2 \
    libxrender1 \
    libxt6 \
    libxtst6 \
    libxxf86vm1 \
    zlib1g \
    xkb-data \
    procps \
    ca-certificates \
    sudo \
    locales \
    locales-all \
    zip \
 && apt-get install -y \
    csh \
    gcc \
    g++ \
    gfortran \
    python3 \
    python3-pip

# Install the AWS CLI to use for staging input and output data
RUN pip3 install awscli

# Set the timezone to avoid warnings in the logs when starting MATLAB
ENV TZ=UTC

# Create directories for the MATLAB install and for the JobStorageLocation
ENV JOB_STORAGE_LOCATION /usr/local/JobStorageLocation
ENV MATLAB_INSTALL_LOCATION /usr/local/matlab
RUN mkdir -p ${MATLAB_INSTALL_LOCATION} ${JOB_STORAGE_LOCATION}
RUN chmod -R +wx ${JOB_STORAGE_LOCATION}

# Remove unneeded cache files
RUN apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# To avoid inadvertantly polluting the / directory, use the JobStorageLocation
# while running MATLAB.
WORKDIR ${JOB_STORAGE_LOCATION}

COPY r2020b/aws-batch/stageDataAndRunJob.sh /usr/local/stageDataAndRunJob.sh
RUN chmod +x /usr/local/stageDataAndRunJob.sh
ENTRYPOINT ["/usr/local/stageDataAndRunJob.sh"]
