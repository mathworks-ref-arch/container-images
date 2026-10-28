# Copyright 2026 The MathWorks, Inc.
ARG BASE_IMAGE=almalinux:8
FROM ${BASE_IMAGE}

LABEL maintainer="The MathWorks, Inc."

ARG TARGETARCH
COPY base-dependencies-${TARGETARCH}.txt /tmp/base-dependencies.txt

RUN yum update --disableplugin=subscription-manager -y \
    && yum install --disableplugin=subscription-manager -y `cat /tmp/base-dependencies.txt` \
    && yum --disableplugin=subscription-manager clean all -y

# To make sure non-ASCII data processed in UTF-8
ENV LANG=en_US.UTF-8
RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb
