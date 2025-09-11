# Copyright 2025 The MathWorks, Inc.
FROM ubuntu:20.04

LABEL maintainer="The MathWorks, Inc."

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb

# Install patched glibc - See https://github.com/mathworks/build-glibc-bz-19329-patch
# Note: base-dependencies.txt includes wget, libcrypt-dev and linux-libc-dev to enable installation of patched -dev packages
WORKDIR /packages
RUN export DEBIAN_FRONTEND=noninteractive &&\
    wget -q https://github.com/mathworks/build-glibc-bz-19329-patch/releases/download/ubuntu-focal/all-packages.tar.gz &&\
    tar -x -f all-packages.tar.gz \
    --exclude glibc-*.deb \
    --exclude libc6-dbg*.deb &&\
    apt-get install --yes --no-install-recommends ./*.deb &&\
    rm -fr /packages
WORKDIR /
