# Copyright 2023 The MathWorks, Inc.
ARG BASE_IMAGE

ARG LOCATION_ROOT=/tmp/deps

FROM ${BASE_IMAGE} as rpm-install
ARG LOCATION_ROOT

# Package noVNC dependencies
ARG LOCATION=${LOCATION_ROOT}/novnc
WORKDIR ${LOCATION}
RUN echo "Install noVNC - HTML5 based VNC viewer" && \
    mkdir -p ${LOCATION}/utils/websockify && \
    wget -qO- https://github.com/novnc/noVNC/archive/v1.0.0.tar.gz | tar xz --strip 1 -C ${LOCATION} && \
    # use older version of websockify to prevent hanging connections on offline containers, see https://github.com/ConSol/docker-headless-vnc-container/issues/50
    wget -qO- https://github.com/novnc/websockify/archive/v0.6.1.tar.gz | tar xz --strip 1 -C ${LOCATION}/utils/websockify && \
    chmod +x -v ${LOCATION}/utils/*.sh && \
    ## create index.html to forward automatically to `vnc_lite.html`
    ln -s $LOCATION/vnc.html $LOCATION/index.html && \
    tar --sort=name --owner=root:0 --group=root:0 --mtime='UTC 1984-12-07' -cf - . | gzip --no-name > ${LOCATION}.tar.gz && \
    sha256sum ${LOCATION}.tar.gz > ${LOCATION}.sha256
ARG VERSION=v1.x
RUN echo "${VERSION}" > ${LOCATION}.version
    
FROM scratch AS export-stage
ARG LOCATION_ROOT

LABEL maintainer="The MathWorks"

COPY --from=rpm-install ${LOCATION_ROOT}/*.gz /
COPY --from=rpm-install ${LOCATION_ROOT}/*.sha256 /
COPY --from=rpm-install ${LOCATION_ROOT}/*.version /
