# Copyright 2020-2024 The MathWorks, Inc.

FROM ubuntu:20.04

LABEL maintainer="The MathWorks, Inc."

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# Uncomment the following RUN apt-get statement if you will be using Simulink 
# code generation capabilities, or if you will be compiling your own mex files
# with gcc, g++, or gfortran.
#
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get install -y gcc g++ gfortran

# Uncomment the following RUN apt-get statement to enable running a program
# that makes use of MATLAB's Engine API for C and Fortran
# https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
#
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get install -y csh

# Uncomment ALL of the following RUN apt-get statement to enable the playing of media files
# (mp3, mp4, etc.) from within MATLAB.
#
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get install --no-install-recommends -y libgstreamer1.0-0 \
# gstreamer1.0-tools \
# gstreamer1.0-libav \
# gstreamer1.0-plugins-base \
# gstreamer1.0-plugins-good \
# gstreamer1.0-plugins-bad \
# gstreamer1.0-plugins-ugly

# Uncomment the following line if you require the fuse filesystem
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get install --no-install-recommends -y libfuse2

# Uncomment the following line if you require network tools
# RUN apt-get install --no-install-recommends -y net-tools

# Uncomment the following line if you require firefox
#RUN export DEBIAN_FRONTEND=noninteractive && apt-get install --no-install-recommends -y firefox

# Uncomment to resolve any license manager issues
# RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3
