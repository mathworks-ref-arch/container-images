# Copyright 2023-2025 The MathWorks, Inc.
ARG BASE_IMAGE

FROM ${BASE_IMAGE} AS base

FROM scratch AS extract-stage

LABEL maintainer="The MathWorks, Inc."

COPY --from=base /*.sha256 /
COPY --from=base /*.version /
