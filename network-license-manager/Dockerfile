# Copyright 2024-2026 The MathWorks, Inc.
FROM rockylinux/rockylinux:9-ubi

RUN yum update -y \
    && yum install -y unzip \
    && yum clean all -y

# Get license manager directly from the mathworks website
ARG MATLAB_RELEASE=R2026a
RUN cd /tmp && \
    curl https://ssd.mathworks.com/supportfiles/downloads/${MATLAB_RELEASE}/license_manager/${MATLAB_RELEASE}/daemons/glnxa64/mathworks_network_license_manager_glnxa64.zip --output mathworks_network_license_manager_glnxa64.zip && \
    unzip mathworks_network_license_manager_glnxa64.zip -d /nlm/ && \
    rm -rf mathworks_network_license_manager_glnxa64.zip

RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3

# Add "lmgr" user in the lmadmin group
RUN groupadd lmadmin && \
    adduser --gid lmadmin --shell /bin/bash --comment "" lmgr

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
