# Copyright 2025 The MathWorks, Inc.
FROM registry.access.redhat.com/ubi8/ubi:latest

LABEL maintainer="The MathWorks, Inc."

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN yum update --disableplugin=subscription-manager -y \
    && yum install --disableplugin=subscription-manager -y `cat /tmp/base-dependencies.txt` \
    && yum --disableplugin=subscription-manager clean all -y

# To make sure non-ASCII data processed in UTF-8
ENV LANG=en_US.UTF-8

RUN [ -s /etc/machine-id ] || dbus-uuidgen > /etc/machine-id
RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb
