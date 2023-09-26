# Copyright 2023 The MathWorks, Inc.
ARG BASE_IMAGE

FROM ${BASE_IMAGE} as base

FROM scratch AS extract-stage

LABEL maintainer="The MathWorks"

COPY --from=base /*.sha256 /
COPY --from=base /*.version /
