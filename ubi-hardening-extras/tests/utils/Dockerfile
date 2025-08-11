# Copyright 2023-2025 The MathWorks, Inc.

ARG BASE_REGISTRY=redhat
ARG BASE_IMAGE=ubi9
ARG BASE_TAG=9.5
ARG IMAGE_UNDER_TEST

FROM ${IMAGE_UNDER_TEST} AS image-under-test

# install the RPM packages contained in the $TAR_IMAGE into a redhat-ubi image

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

ARG RPM_INSTALL=/tmp

COPY --from=image-under-test *.rpm.tar.gz ${RPM_INSTALL}

RUN cd ${RPM_INSTALL} && \
    ls *.rpm.tar.gz | xargs -n 1 tar -xvzf && \
    dnf install -y --nodocs *.rpm --nogpgcheck && \
    dnf -y clean all && \
    rm -rf /var/cache/dnf && \
    rm -rf ${RPM_INSTALL}
