# Copyright 2024-2025 The MathWorks, Inc.
ARG BASE_IMAGE

ARG MPM_DOWNLOAD_DESTINATION="/usr/local/src"

ARG MATLAB_RELEASE=R2025b

ARG LOCATION_ROOT=/tmp/deps

FROM ${BASE_IMAGE} AS matlab-download

ARG LOCATION_ROOT
ARG MATLAB_RELEASE
ARG MPM_DOWNLOAD_DESTINATION

ARG DNF="dnf --disableplugin subscription-manager --assumeyes"
RUN ${DNF} update && \
    ${DNF} install ca-certificates wget

RUN wget -q https://www.mathworks.com/mpm/glnxa64/mpm && \
    chmod +x mpm && \
    ./mpm download \
    --release=${MATLAB_RELEASE} \
    --destination=${MPM_DOWNLOAD_DESTINATION} \
    --products MATLAB \
    && chmod +x ${MPM_DOWNLOAD_DESTINATION}/mpm/glnxa64/mpm \
    || (echo "MPM Download Failure. See below for more information:" && cat /tmp/mathworks_root.log && false)

ARG VERSION=v1.x

RUN mkdir -p ${LOCATION_ROOT} && \
    sha256sum ${MPM_DOWNLOAD_DESTINATION}/ProductFilesInfo.xml > ${LOCATION_ROOT}/matlab.sha256 && \
    echo "${VERSION}" > ${LOCATION_ROOT}/matlab.version

# Move MPM and the installation files to a scratch image
FROM scratch

LABEL maintainer="The MathWorks, Inc."

# Declare build arguments to use at the current build stage.
ARG MPM_DOWNLOAD_DESTINATION
ARG LOCATION_ROOT

COPY --from=matlab-download ${MPM_DOWNLOAD_DESTINATION} /
COPY --from=matlab-download ${LOCATION_ROOT}/*.sha256 /
COPY --from=matlab-download ${LOCATION_ROOT}/*.version /
