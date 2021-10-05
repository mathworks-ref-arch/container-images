# Copyright 2021 The MathWorks, Inc.
FROM registry.access.redhat.com/ubi8/ubi:latest

LABEL maintainer="The MathWorks"

ENV TZ="Etc/UTC"

RUN yum update --disableplugin=subscription-manager -y && yum install --disableplugin=subscription-manager -y \
alsa-lib.x86_64 \
at-spi2-atk.x86_64 \
at-spi2-core.x86_64 \
atk.x86_64 \
cairo.x86_64 \
cairo-gobject.x86_64 \
cups-libs.x86_64 \
dbus-libs.x86_64 \
fontconfig.x86_64 \
gdk-pixbuf2.x86_64 \
glib2.x86_64 \
glibc.x86_64 \
glibc-langpack-en.x86_64 \
glibc-locale-source.x86_64 \
gtk3.x86_64 \
libSM.x86_64 \
libX11.x86_64 \
libX11-xcb.x86_64 \
libXcomposite.x86_64 \
libXcursor.x86_64 \
libXdamage.x86_64 \
libXext.x86_64 \
libXfixes.x86_64 \
libXft.x86_64 \
libXi.x86_64 \
libXinerama.x86_64 \
libXrandr.x86_64 \
libXrender.x86_64 \
libXt.x86_64 \
libXtst.x86_64 \
libXxf86vm.x86_64 \
libcap.x86_64 \
libdrm.x86_64 \
libgomp.x86_64 \
libsndfile.x86_64 \
libuuid.x86_64 \
libxcb.x86_64 \
libxcrypt.x86_64 \
make.x86_64 \
mesa-libgbm.x86_64 \
net-tools.x86_64 \
nspr.x86_64 \
nss.x86_64 \
nss-util.x86_64 \
openssl-libs.x86_64 \
pam.x86_64 \
pango.x86_64 \
procps-ng.x86_64 \
python39-libs.x86_64 \
sudo.x86_64 \
unixODBC.x86_64 \
unzip.x86_64 \
zlib.x86_64 \
&& yum --disableplugin=subscription-manager clean all -y

ENV LANG C
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
 
# Unlike Redhat8/CentOS8, ubi8 does not provide libnsl version 1, so get libnsl2 and make soft link.
RUN yum upgrade --disableplugin=subscription-manager -y \
&& yum --disableplugin=subscription-manager install libnsl2.x86_64 -y  \
&& yum --disableplugin=subscription-manager clean all -y \
&& ln -s libnsl.so.2 /usr/lib64/libnsl.so.1
