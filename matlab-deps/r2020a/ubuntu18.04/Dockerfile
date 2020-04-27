# Copyright 2020 The MathWorks, Inc.

FROM ubuntu:18.04

MAINTAINER MathWorks

RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    libasound2 \
    libatk1.0-0 \
    libavcodec-extra57 \
    libavformat57 \
    libc6 \
    libcairo-gobject2 \
    libcairo2 \
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
    libpython3.6 \
    libpython3.7 \
    libselinux1 \
    libsm6 \
    libsndfile1 \
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
    locales \
    locales-all \
    procps \
    sudo \
    unzip \
    xkb-data \
    zlib1g

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

# Uncomment or customize the following lines to build a docker image that runs matlab on entry
#ENV PATH="/usr/local/MATLAB/R2020a/bin:${PATH}"
#ENTRYPOINT ["matlab"]

# To avoid inadvertantly polluting the / directory, use root's home directory
# while running MATLAB.
WORKDIR /root
