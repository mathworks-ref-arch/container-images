# Copyright 2020-2021 The MathWorks, Inc.

FROM ubuntu:18.04

LABEL maintainer="The MathWorks"

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

COPY base-dependencies.txt /tmp/base-dependencies.txt

RUN apt-get update && apt-get install --no-install-recommends -y `cat /tmp/base-dependencies.txt` \
    && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following RUN apt-get statement to install extended locale support for MATLAB
#RUN apt-get install -y locales locales-all

# Uncomment the following RUN ln -s statement if you will be running the MATLAB
# license manager INSIDE the container.
#RUN ln -s ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3

# Uncomment the following RUN apt-get statement if you will be using Simulink
# code generation capabilities, or if you will be using mex with gcc, g++,
# or gfortran.
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
#RUN apt-get install -y libgstreamer1.0-0 \
# gstreamer1.0-tools \
# gstreamer1.0-libav \
# gstreamer1.0-plugins-base \
# gstreamer1.0-plugins-good \
# gstreamer1.0-plugins-bad \
# gstreamer1.0-plugins-ugly \
# gstreamer1.0-doc

# Uncomment the following RUN apt-get statement if you will be using the 32-bit tcc compiler
# used in the Polyspace product line.
#RUN apt-get install -y libc6-i386
