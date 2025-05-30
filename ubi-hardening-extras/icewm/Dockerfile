# Copyright 2023-2025 The MathWorks, Inc.
ARG BASE_IMAGE

ARG LOCATION_ROOT=/tmp/deps

FROM ${BASE_IMAGE} AS rpm-install
ARG LOCATION_ROOT

# Package iceWM dependencies
ARG LOCATION=${LOCATION_ROOT}/icewm
WORKDIR ${LOCATION}
ENV DNF="dnf --disableplugin subscription-manager --assumeyes"
RUN ${DNF} download icewm --resolve && \
    ${DNF} localinstall *.rpm && \
    tar --sort=name --owner=root:0 --group=root:0 --mtime='UTC 1984-12-07' -cf - *.rpm | gzip --no-name > ${LOCATION}.rpm.tar.gz && \
    sha256sum ${LOCATION}.rpm.tar.gz > ${LOCATION}.sha256
ARG VERSION=v1.x
RUN echo "${VERSION}" > ${LOCATION}.version

FROM scratch AS export-stage
ARG LOCATION_ROOT

LABEL maintainer="The MathWorks, Inc."

COPY --from=rpm-install ${LOCATION_ROOT}/*.gz /
COPY --from=rpm-install ${LOCATION_ROOT}/*.sha256 /
COPY --from=rpm-install ${LOCATION_ROOT}/*.version /
