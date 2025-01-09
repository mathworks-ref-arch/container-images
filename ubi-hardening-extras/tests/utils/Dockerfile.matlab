# Copyright 2023-2024 The MathWorks, Inc.

ARG BASE_REGISTRY=redhat
ARG BASE_IMAGE=ubi9
ARG BASE_TAG=9.4
ARG IMAGE_UNDER_TEST=matlab

FROM ${IMAGE_UNDER_TEST} AS image-under-test

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

ARG MATLAB_INSTALL_LOCATION=/opt/matlab

COPY --from=image-under-test / /matlab-archive

RUN /matlab-archive/mpm/glnxa64/mpm install \
    --source=/matlab-archive/archives \
    --destination=${MATLAB_INSTALL_LOCATION} \
    --products MATLAB \
    || (echo "MPM Installation Failure. See below for more information:" && cat /tmp/mathworks_root.log && false) \
    && rm -rf /tmp/mathworks_root.log \
    && ln -s ${MATLAB_INSTALL_LOCATION}/bin/matlab /usr/local/bin/matlab
