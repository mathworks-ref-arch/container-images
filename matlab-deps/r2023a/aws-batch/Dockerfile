# Copyright 2023-2025 The MathWorks, Inc.

FROM nvidia/cuda:11.8.0-base-ubuntu20.04

LABEL maintainer="The MathWorks, Inc."

# base-dependencies.txt lists libraries required by MATLAB, except for:
# csh                  - Support MATLAB's Engine API for C and Fortran. See https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
# gcc, g++, gfortran   - Support Simulink code generation and mex with gcc, g++, or gfortran.
# locales, locales-all - Provide extended locales support
# python3, python3-pip - Python and pip are to run/install the AWS CLI.
# unzip, zip           - Used to stage input/output data.
COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# Install patched glibc - See https://github.com/mathworks/build-glibc-bz-19329-patch
# Note: base-dependencies.txt includes libcrypt-dev and linux-libc-dev to enable installation of patched -dev packages
WORKDIR /packages
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get clean && apt-get autoremove && \
    wget -q https://github.com/mathworks/build-glibc-bz-19329-patch/releases/download/ubuntu-focal/all-packages.tar.gz && \
    tar -x -f all-packages.tar.gz \
    --exclude glibc-*.deb \
    --exclude libc6-dbg*.deb && \
    apt-get install --yes --no-install-recommends --allow-downgrades ./*.deb && \
    rm -fr /packages
WORKDIR /

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

COPY stageDataAndRunJob.sh /usr/local/stageDataAndRunJob.sh
RUN chmod +x /usr/local/stageDataAndRunJob.sh

# To make sure non-ASCII data processed in UTF-8
ENV LANG=en_US.UTF-8

ENTRYPOINT ["/usr/local/stageDataAndRunJob.sh"]
