# Copyright 2020 The MathWorks, Inc.

FROM ubuntu:20.04

MAINTAINER The MathWorks

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

RUN apt-get update && apt-get install --no-install-recommends -y \
libasound2 \
libatk1.0-0 \
libc6 \
libcairo-gobject2 \
libcairo2 \
libcrypt1 \
libcups2 \
libdbus-1-3 \
libfontconfig1 \
libgdk-pixbuf2.0-0 \
libgstreamer-plugins-base1.0-0 \
libgstreamer1.0-0 \
libgtk-3-0 \
libnspr4 \
libnss3 \
libpam0g \
libpango-1.0-0 \
libpangocairo-1.0-0 \
libpangoft2-1.0-0 \
libpython2.7 \
libpython3.8 \
libselinux1 \
libsm6 \
libsndfile1 \
libtcl8.6 \
libuuid1 \
libx11-6 \
libx11-xcb1 \
libxcb1 \
libxcomposite1 \
libxcursor1 \
libxdamage1 \
libxext6 \
libxfixes3 \
libxft2 \
libxi6 \
libxinerama1 \
libxrandr2 \
libxrender1 \
libxt6 \
libxtst6 \
libxxf86vm1 \
zlib1g \
xkb-data \
procps \
ca-certificates \
sudo \
locales locales-all

# Uncomment the following RUN apt-get statement if you will be using Simulink 
# code generation capabilities, or if you will be compiling your own mex files
# with gcc, g++, or gfortran.
#
#RUN apt-get install -y gcc g++ gfortran

# Uncomment the following RUN apt-get statement to enable running a program
# that makes use of MATLAB's Engine API for C and Fortran
# https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
#
#RUN apt-get install -y csh

# Uncomment ALL of the following RUN apt-get statement to enable the playing of media files
# (mp3, mp4, etc.) from within MATLAB.
#
#RUN apt-get install --no-install-recommends -y libgstreamer1.0-0 \
# gstreamer1.0-tools \
# gstreamer1.0-libav \
# gstreamer1.0-plugins-base \
# gstreamer1.0-plugins-good \
# gstreamer1.0-plugins-bad \
# gstreamer1.0-plugins-ugly

# Uncomment the following line if you require the fuse filesystem
#RUN apt-get install --no-install-recommends -y libfuse2

# Uncomment the following line if you require network tools
RUN apt-get install --no-install-recommends -y net-tools

# Uncomment the following line if you require firefox
#RUN apt-get install --no-install-recommends -y firefox

# Required for license manager
RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3

# Remove unneeded cache files
RUN apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*
