# Copyright 2024 The MathWorks, Inc.

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN apt-get update && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb
