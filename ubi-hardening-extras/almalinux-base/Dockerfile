# Copyright 2023 The MathWorks, Inc.
ARG BASE_IMAGE=almalinux
ARG BASE_TAG=8.9

FROM ${BASE_IMAGE}:${BASE_TAG}

LABEL maintainer="The MathWorks"

ARG LOCATION_ROOT=/tmp

COPY base-dependencies.txt ${LOCATION_ROOT}
ARG DNF="dnf --disableplugin subscription-manager --assumeyes"
RUN ${DNF} update && \
    ${DNF} install $(cat ${LOCATION_ROOT}/base-dependencies.txt)

RUN ${DNF} install dnf-plugins-core epel-release
