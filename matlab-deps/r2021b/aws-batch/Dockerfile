# Copyright 2021 The MathWorks, Inc.

FROM nvidia/cuda:11.4.1-base-ubuntu20.04

LABEL maintainer="The MathWorks"

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

# The following libraries are all required by MATLAB, except for:
# csh                  - Support MATLAB's Engine API for C and Fortran. See https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
# gcc, g++, gfortran   - Support Simulink code generation and mex with gcc, g++, or gfortran.
# locales, locales-all - Provide extended locales support
# python3, python3-pip - Python and pip are to run/install the AWS CLI.
# unzip, zip           - Used to stage input/output data.
RUN apt-get update && apt-get install --no-install-recommends -y \
   ca-certificates \
   libasound2 \
   libatk-bridge2.0-0 \
   libatk1.0-0 \
   libatspi2.0-0 \
   libc6 \
   libcairo2 \
   libcairo-gobject2 \
   libcap2 \
   libcrypt1 \
   libcups2 \
   libdbus-1-3 \
   libdrm2 \
   libfontconfig1 \
   libgbm1 \
   libgdk-pixbuf2.0-0 \
   libglib2.0-0 \
   libgomp1 \
   libgstreamer1.0-0 \
   libgstreamer-plugins-base1.0-0 \
   libgtk-3-0 \
   libnspr4 \
   libnss3 \
   libodbc1 \
   libpam0g \
   libpango-1.0-0 \
   libpangocairo-1.0-0 \
   libpangoft2-1.0-0 \
   libpython3.9 \
   libsm6 \
   libsndfile1 \
   libssl1.1 \
   libuuid1 \
   libx11-6 \
   libx11-xcb1 \
   libxcb-dri3-0 \
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
   locales \
   locales-all \
   make \
   net-tools \
   procps \
   sudo \
   tzdata \
   unzip \
   zip \
   zlib1g \
 && apt-get install -y \
    csh \
    gcc \
    g++ \
    gfortran \
    python3 \
    python3-pip \
 && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Install the AWS CLI to use for staging input and output data
RUN pip3 install awscli

# Create directories for the MATLAB install and for the JobStorageLocation
ENV JOB_STORAGE_LOCATION /usr/local/JobStorageLocation
ENV MATLAB_INSTALL_LOCATION /usr/local/matlab
RUN mkdir -p ${MATLAB_INSTALL_LOCATION} ${JOB_STORAGE_LOCATION}
RUN chmod -R +wx ${JOB_STORAGE_LOCATION}

# To avoid inadvertantly polluting the / directory, use the JobStorageLocation
# while running MATLAB.
WORKDIR ${JOB_STORAGE_LOCATION}

COPY r2021b/aws-batch/stageDataAndRunJob.sh /usr/local/stageDataAndRunJob.sh
RUN chmod +x /usr/local/stageDataAndRunJob.sh
ENTRYPOINT ["/usr/local/stageDataAndRunJob.sh"]
