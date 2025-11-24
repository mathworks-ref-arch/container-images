# Copyright 2023-2025 The MathWorks, Inc.
ARG BASE_IMAGE=almalinux
ARG BASE_TAG=9.7

FROM ${BASE_IMAGE}:${BASE_TAG}

LABEL maintainer="The MathWorks, Inc."

ARG LOCATION_ROOT=/tmp

COPY base-dependencies.txt ${LOCATION_ROOT}
ARG DNF="dnf --disableplugin subscription-manager --assumeyes"
RUN ${DNF} update && \
    ${DNF} install $(cat ${LOCATION_ROOT}/base-dependencies.txt)

RUN ${DNF} install dnf-plugins-core epel-release
