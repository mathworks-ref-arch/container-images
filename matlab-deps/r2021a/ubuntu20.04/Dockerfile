# Copyright 2021 The MathWorks, Inc.

FROM ubuntu:20.04

LABEL maintainer="The MathWorks"

ENV DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC"

RUN apt-get update && apt-get install --no-install-recommends -y \
ca-certificates \
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
libodbc1 \
libpam0g \
libpango-1.0-0 \
libpangocairo-1.0-0 \
libpangoft2-1.0-0 \
libpython2.7 \
libpython3.8 \
libselinux1 \
libsm6 \
libsndfile1 \
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
locales \
locales-all \
make \
net-tools \
procps \
sudo \
tzdata \
unzip \
zlib1g \
&& apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb

# Uncomment the following RUN apt-get statement if you will be using Simulink 
# code generation capabilities, or if you will be compiling your own mex files
# with gcc, g++, or gfortran.
#
#RUN apt-get update -y && apt-get install -y gcc g++ gfortran && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following RUN apt-get statement to enable running a program
# that makes use of MATLAB's Engine API for C and Fortran
# https://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
#
#RUN apt-get update -y && apt-get install -y csh && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment ALL of the following RUN apt-get statement to enable the playing of media files
# (mp3, mp4, etc.) from within MATLAB.
#
#RUN apt-get update -y && apt-get install --no-install-recommends -y libgstreamer1.0-0 \
# gstreamer1.0-tools \
# gstreamer1.0-libav \
# gstreamer1.0-plugins-base \
# gstreamer1.0-plugins-good \
# gstreamer1.0-plugins-bad \
# gstreamer1.0-plugins-ugly \
# && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following line if you require the fuse filesystem
#RUN apt-get update -y && apt-get install --no-install-recommends -y libfuse2 && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment the following line if you require firefox
#RUN apt-get update -y && apt-get install --no-install-recommends -y firefox && apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# Uncomment to resolve license manager issues
#RUN ln -s /lib64/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3
