# Copyright 2020-2023 The MathWorks, Inc.

FROM nvidia/cuda:11.8.0-base-ubuntu20.04

LABEL maintainer="The MathWorks, Inc."

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

# base-dependencies.txt lists libraries required by MATLAB, except for:
# csh                  - Support MATLAB's Engine API for C and Fortran. See https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
# gcc, g++, gfortran   - Support Simulink code generation and mex with gcc, g++, or gfortran.
# locales, locales-all - Provide extended locales support
# python3, python3-pip - Python and pip are to run/install the AWS CLI.
# unzip, zip           - Used to stage input/output data.
COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN apt-get update && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*


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

COPY stageDataAndRunJob.sh /usr/local/stageDataAndRunJob.sh
RUN chmod +x /usr/local/stageDataAndRunJob.sh
ENTRYPOINT ["/usr/local/stageDataAndRunJob.sh"]
