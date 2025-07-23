# MATLAB Dependencies

These images include the dependencies required to run MATLAB®, Simulink®, and other MathWorks products.

**Note: These images do not include MATLAB. To use a prebuild MATLAB container image, see the [MATLAB Container Image](https://hub.docker.com/r/mathworks/matlab) on Docker Hub. To build your own MATLAB container image, follow [these instructions](https://github.com/mathworks-ref-arch/matlab-dockerfile).**

## Base Operating System Update Policy
The default image for each MATLAB release is based on the latest Ubuntu Long Term Support base image.

To use an image based on a fixed Ubuntu base image instead, use the appropriate tag by referring to the table.

When a base image is no longer supported by Ubuntu, the 'matlab-deps' image based on these images will be removed from Docker Hub. You can however still build your own container images using the source Dockerfiles available in the [MathWorks Container Images Repository](https://github.com/mathworks-ref-arch/container-images/tree/main/matlab-deps).

## Supported Tags

| Tags         | MATLAB Version | Operating System | Base Image | Usage Notes |
| ------------ | -------------- | ---------------- |----------- | ----------- |
|[`latest`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/ubuntu24.04/Dockerfile) | R2025a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2025a`, `R2025a`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/ubuntu24.04/Dockerfile) | R2025a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2025a-ubuntu24.04`, `R2025a-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/ubuntu24.04/Dockerfile) | R2025a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2025a-ubuntu22.04`, `R2025a-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/ubuntu22.04/Dockerfile) | R2025a | Ubuntu 22.04 | ubuntu:22.04 | |
|[`r2025a-ubi9`, `R2025a-ubi9`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/ubi9/Dockerfile) | R2025a | Red Hat UBI 9 | registry.access.redhat.​com/ubi9/ubi:latest | |
|[`r2025a-ubi8`, `R2025a-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/ubi8/Dockerfile) | R2025a | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2025a-aws-batch`, `R2025a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2025a/aws-batch/Dockerfile) | R2025a | Ubuntu 22.04 | nvidia/cuda:12.2.2-base-ubuntu22.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2024b`, `R2024b`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubuntu22.04/Dockerfile) | R2024b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2024b-ubuntu24.04`, `R2024b-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubuntu24.04/Dockerfile) | R2024b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2024b-ubuntu22.04`, `R2024b-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubuntu22.04/Dockerfile) | R2024b | Ubuntu 22.04 | ubuntu:22.04 | |
|⚠️ [`r2024b-ubuntu20.04`, `R2024b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubuntu20.04/Dockerfile) | R2024b | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2024b-ubi9`, `R2024b-ubi9`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubi9/Dockerfile) | R2024b | Red Hat UBI 9 | registry.access.redhat.​com/ubi9/ubi:latest | |
|[`r2024b-ubi8`, `R2024b-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/ubi8/Dockerfile) | R2024b | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2024b-aws-batch`, `R2024b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024b/aws-batch/Dockerfile) | R2024b | Ubuntu 22.04 | nvidia/cuda:12.2.2-base-ubuntu22.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2024a`, `R2024a`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/ubuntu22.04/Dockerfile) | R2024a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2024a-ubuntu24.04`, `R2024a-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/ubuntu24.04/Dockerfile) | R2024a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2024a-ubuntu22.04`, `R2024a-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/ubuntu22.04/Dockerfile) | R2024a | Ubuntu 22.04 | ubuntu:22.04 | |
|⚠️ [`r2024a-ubuntu20.04`, `R2024a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/ubuntu20.04/Dockerfile) | R2024a | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2024a-ubi9`, `R2024a-ubi9`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/ubi9/Dockerfile) | R2024a | Red Hat UBI 9 | registry.access.redhat.​com/ubi9/ubi:latest | |
|[`r2024a-ubi8`, `R2024a-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/ubi8/Dockerfile) | R2024a | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2024a-aws-batch`, `R2024a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2024a/aws-batch/Dockerfile) | R2024a | Ubuntu 22.04 | nvidia/cuda:12.2.2-base-ubuntu22.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2023b`, `R2023b`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/ubuntu22.04/Dockerfile) | R2023b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2023b-ubuntu24.04`, `R2023b-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/ubuntu24.04/Dockerfile) | R2023b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2023b-ubuntu22.04`, `R2023b-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/ubuntu22.04/Dockerfile) | R2023b | Ubuntu 22.04 | ubuntu:22.04 | |
|⚠️ [`r2023b-ubuntu20.04`, `R2023b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/ubuntu20.04/Dockerfile) | R2023b | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2023b-ubi9`, `R2023b-ubi9`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/ubi9/Dockerfile) | R2023b | Red Hat UBI 9 | registry.access.redhat.​com/ubi9/ubi:latest | |
|[`r2023b-ubi8`, `R2023b-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/ubi8/Dockerfile) | R2023b | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2023b-aws-batch`, `R2023b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023b/aws-batch/Dockerfile) | R2023b | Ubuntu 22.04 | nvidia/cuda:11.8.0-base-ubuntu22.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2023a`, `R2023a`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/ubuntu20.04/Dockerfile) | R2023a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2023a-ubuntu24.04`, `R2023a-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/ubuntu24.04/Dockerfile) | R2023a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2023a-ubuntu22.04`, `R2023a-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/ubuntu22.04/Dockerfile) | R2023a | Ubuntu 22.04 | ubuntu:22.04 | |
|⚠️ [`r2023a-ubuntu20.04`, `R2023a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/ubuntu20.04/Dockerfile) | R2023a | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2023a-ubi8`, `R2023a-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/ubi8/Dockerfile) | R2023a | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2023a-ubi9`, `R2023a-ubi9`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/ubi8/Dockerfile) | R2023a | Red Hat UBI 9 | registry.access.redhat.​com/ubi9/ubi:latest | |
|[`r2023a-aws-batch`, `R2023a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2023a/aws-batch/Dockerfile) | R2023a | Ubuntu 20.04 | nvidia/cuda:11.8.0-base-ubuntu20.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2022b`, `R2022b`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/ubuntu20.04/Dockerfile) | R2022b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2022b-ubuntu24.04`, `R2022b-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/ubuntu24.04/Dockerfile) | R2022b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2022b-ubuntu22.04`, `R2022b-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/ubuntu22.04/Dockerfile) | R2022b | Ubuntu 22.04 | ubuntu:22.04 | |
|⚠️ [`r2022b-ubuntu20.04`, `R2022b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/ubuntu20.04/Dockerfile) | R2022b | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2022b-ubi8`, `R2022b-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/ubi8/Dockerfile) | R2022b | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2022b-ubi9`, `R2022b-ubi9`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/ubi9/Dockerfile) | R2022b | Red Hat UBI 9 | registry.access.redhat.​com/ubi9/ubi:latest | |
|[`r2022b-aws-batch`, `R2022b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022b/aws-batch/Dockerfile) | R2022b | Ubuntu 20.04 | nvidia/cuda:11.8.0-base-ubuntu20.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2022a`, `R2022a`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022a/ubuntu20.04/Dockerfile) | R2022a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2022a-ubuntu24.04`, `R2022a-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022a/ubuntu24.04/Dockerfile) | R2022a | Ubuntu 24.04 | ubuntu:24.04 | |
|⚠️ [`r2022a-ubuntu20.04`, `R2022a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022a/ubuntu20.04/Dockerfile) | R2022a | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2022a-ubi8`, `R2022a-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022a/ubi8/Dockerfile) | R2022a | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2022a-aws-batch`, `R2022a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2022a/aws-batch/Dockerfile) | R2022a | Ubuntu 20.04 | nvidia/cuda:11.8.0-base-ubuntu20.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2021b`, `R2021b`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021b/ubuntu20.04/Dockerfile) | R2021b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2021b-ubuntu24.04`, `R2021b-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021b/ubuntu24.04/Dockerfile) | R2021b | Ubuntu 24.04 | ubuntu:24.04 | |
|⚠️ [`r2021b-ubuntu20.04`, `R2021b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021b/ubuntu20.04/Dockerfile) | R2021b | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2021b-ubi8`, `R2021b-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021b/ubi8/Dockerfile) | R2021b | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2021b-aws-batch`, `R2021b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021b/aws-batch/Dockerfile) | R2021b | Ubuntu 20.04 | nvidia/cuda:11.8.0-base-ubuntu20.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2021a`, `R2021a`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021a/ubuntu20.04/Dockerfile) | R2021a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2021a-ubuntu24.04`, `R2021a-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021a/ubuntu24.04/Dockerfile) | R2021a | Ubuntu 24.04 | ubuntu:24.04 | |
|⚠️ [`r2021a-ubuntu20.04`, `R2021a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021a/ubuntu20.04/Dockerfile) | R2021a | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2021a-aws-batch`, `R2021a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2021a/aws-batch/Dockerfile) | R2021a | Ubuntu 20.04 | nvidia/cuda:11.8.0-base-ubuntu20.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2020b`, `R2020b`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020b/ubuntu20.04/Dockerfile) | R2020b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2020b-ubuntu24.04`, `R2020b-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020b/ubuntu24.04/Dockerfile) | R2020b | Ubuntu 24.04 | ubuntu:24.04 | |
|⚠️ [`r2020b-ubuntu20.04`, `R2020b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020b/ubuntu20.04/Dockerfile) | R2020b | Ubuntu 20.04 | ubuntu:20.04 | This image will be removed in August 2025. |
|[`r2020b-aws-batch`, `R2020b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020b/aws-batch/Dockerfile) | R2020b | Ubuntu 20.04 | nvidia/cuda:11.8.0-base-ubuntu20.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2020a`, `R2020a`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020a/ubuntu18.04/Dockerfile) | R2020a | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2020a-ubuntu24.04`, `R2020a-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020a/ubuntu24.04/Dockerfile) | R2020a | Ubuntu 24.04 | ubuntu:24.04 | |
|⚠️ [`r2020a-ubuntu18.04`, `R2020a-ubuntu18.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020a/ubuntu18.04/Dockerfile) | R2020a | Ubuntu 18.04 | ubuntu:18.04 | This image will be removed in August 2025. |
|[`r2020a-aws-batch`, `R2020a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2020a/aws-batch/Dockerfile) | R2020a | Ubuntu 18.04 | nvidia/11.8.0-base-ubuntu18.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |
|[`r2019b`, `R2019b`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2019b/ubuntu18.04/Dockerfile) | R2019b | Ubuntu 24.04 | ubuntu:24.04 | |
|[`r2019b-ubuntu24.04`, `R2019b-ubuntu24.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2019b/ubuntu24.04/Dockerfile) | R2019b | Ubuntu 24.04 | ubuntu:24.04 | |
|⚠️ [`r2019b-ubuntu18.04`, `R2019b-ubuntu18.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2019b/ubuntu18.04/Dockerfile) | R2019b | Ubuntu 18.04 | ubuntu:18.04 | This image will be removed in August 2025. |
|[`r2019b-aws-batch`, `R2019b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/main/matlab-deps/r2019b/aws-batch/Dockerfile) | R2019b | Ubuntu 18.04 | nvidia/cuda:11.8.0-base-ubuntu18.04 | Use this image with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch). |

## License
The license for this container is available [here](https://github.com/mathworks-ref-arch/container-images/blob/main/LICENSE.md).

## Security Reporting
To report suspected security issues, follow [these instructions](https://github.com/mathworks-ref-arch/container-images/blob/main/SECURITY.md).

## Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

----

Copyright 2019-2025 The MathWorks, Inc.

----