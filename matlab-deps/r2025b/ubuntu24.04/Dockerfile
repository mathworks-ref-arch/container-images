# Copyright 2025 The MathWorks, Inc.
FROM ubuntu:24.04

LABEL maintainer="The MathWorks"

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb

# To make sure non-ASCII data processed in UTF-8
ENV LANG=en_US.UTF-8

WORKDIR /
