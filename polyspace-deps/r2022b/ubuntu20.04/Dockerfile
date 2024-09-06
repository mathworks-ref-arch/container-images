# Copyright 2022 The MathWorks, Inc.
FROM ubuntu:20.04

LABEL maintainer="The MathWorks, Inc."

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN apt-get update && \
    apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` && \
    apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

