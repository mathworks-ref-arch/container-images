# Copyright 2024 The MathWorks, Inc.
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

# Uncomment the following RUN apt-get statement if you will be using Simulink 
# code generation capabilities, or if you will be compiling your own mex files
# with gcc, g++, or gfortran.
#
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install -y gcc g++ gfortran && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following RUN apt-get statement to enable running a program
# that makes use of MATLAB's Engine API for C and Fortran
# https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
#
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install -y csh && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment ALL of the following RUN apt-get statement to enable the playing of media files
# (mp3, mp4, etc.) from within MATLAB.
#
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install --no-install-recommends -y libgstreamer1.0-0 \
# gstreamer1.0-tools \
# gstreamer1.0-libav \
# gstreamer1.0-plugins-base \
# gstreamer1.0-plugins-good \
# gstreamer1.0-plugins-bad \
# gstreamer1.0-plugins-ugly \
# && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following line if you require the fuse filesystem
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install --no-install-recommends -y libfuse2 && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following line if you require firefox
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install --no-install-recommends -y firefox && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment to resolve any license manager issues
#RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3
