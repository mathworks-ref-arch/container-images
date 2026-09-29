# Copyright 2024-2026 The MathWorks, Inc.

FROM scratch AS src
COPY runtime /runtime

FROM rockylinux/rockylinux:9-ubi

RUN yum update -y \
    && yum install -y unzip perl \
    && yum clean all -y

# Get license manager directly from the mathworks website or from a file in the context
ARG MATLAB_RELEASE=R2026a
ARG ZIP_SOURCE=https://ssd.mathworks.com/supportfiles/downloads/${MATLAB_RELEASE}/license_manager/${MATLAB_RELEASE}/daemons/glnxa64/mathworks_network_license_manager_glnxa64.zip
ADD ${ZIP_SOURCE} /tmp/mathworks_network_license_manager_glnxa64.zip
RUN unzip /tmp/mathworks_network_license_manager_glnxa64.zip -d /nlm/ && \
    rm -rf /tmp/mathworks_network_license_manager_glnxa64.zip

RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3

# Add "lmgr" user in the lmadmin group
RUN groupadd lmadmin && \
    adduser --gid lmadmin --shell /bin/bash --comment "" lmgr

COPY --from=src runtime /

# Add extra MLM options
ARG EXTRA_MLM_OPTS
RUN if [[ ! -z "${EXTRA_MLM_OPTS}" ]]; then \
    echo -e "${EXTRA_MLM_OPTS}" >> /opt/mlm.opt; \
    fi

ENTRYPOINT ["/docker-entrypoint.sh"]
