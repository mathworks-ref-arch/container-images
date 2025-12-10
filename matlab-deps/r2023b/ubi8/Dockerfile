# Copyright 2023 The MathWorks, Inc.
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

# Uncomment the following RUN yum statement to enable code generation capabilities,
# or if you will be compiling your own mex files with gcc, g++, or gfortran.
#
#RUN yum install -y gcc.x86_64 gcc-c++.x86_64 gcc-gfortran.x86_64 && yum --disableplugin=subscription-manager clean all -y

# Uncomment the following line if you require the fuse filesystem
#RUN yum install -y fuse-libs.x86_64 && yum --disableplugin=subscription-manager clean all -y

# Uncomment to resolve certain license manager issues
#RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3
