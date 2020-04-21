# Copyright 2020 The MathWorks, Inc.

FROM nvidia/cuda:10.1-base

MAINTAINER MathWorks

# The following libraries are all required by MATLAB, except for:
# csh                  - Support MATLAB's Engine API for C and Fortran. See https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
# gcc, g++, gfortran   - Support Simulink code generation and mex with gcc, g++, or gfortran.
# locales, locales-all - Provide extended locales support
# python3, python3-pip - Python and pip are to run/install the AWS CLI.
# unzip, zip           - Used to stage input/output data.
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    libasound2 \
    libatk1.0-0 \
    libavcodec-extra57 \
    libavformat57 \
    libc6 \
    libcairo-gobject2 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdbus-glib-1-2 \
    libfontconfig1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libgnomevfs2-0 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libgtk-3-0 \
    libidl-2-0 \
    libnss3 \
    libpam0g \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libpython2.7 \
    libpython3.6 \
    libpython3.7 \
    libselinux1 \
    libsm6 \
    libsndfile1 \
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
    libxss1 \
    libxt6 \
    libxtst6 \
    libxxf86vm1 \
    procps \
    sudo \
    unzip \
    xkb-data \
    zip \
    zlib1g \
 && apt-get install -y \
    csh \
    gcc \
    g++ \
    gfortran \
    locales \
    locales-all \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Install the AWS CLI to use for staging input and output data
RUN pip3 install awscli

# Set the timezone to avoid warnings in the logs when starting MATLAB
ENV TZ=UTC

# Create directories for the MATLAB install and for the JobStorageLocation
ENV JOB_STORAGE_LOCATION /usr/local/JobStorageLocation
ENV MATLAB_INSTALL_LOCATION /usr/local/matlab
RUN mkdir -p ${MATLAB_INSTALL_LOCATION} ${JOB_STORAGE_LOCATION}
RUN chmod -R +wx ${JOB_STORAGE_LOCATION}

# To avoid inadvertantly polluting the / directory, use the JobStorageLocation
# while running MATLAB.
WORKDIR ${JOB_STORAGE_LOCATION}

COPY r2019b/aws-batch/stageDataAndRunJob.sh /usr/local/stageDataAndRunJob.sh
RUN chmod +x /usr/local/stageDataAndRunJob.sh
ENTRYPOINT ["/usr/local/stageDataAndRunJob.sh"]
