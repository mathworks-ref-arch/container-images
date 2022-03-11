# MATLAB Dependencies

This container includes the dependencies required to run MATLAB®, Simulink®, and other MathWorks products.

**Note: This container does not include MATLAB.  To build a MATLAB container, follow [these instructions](https://github.com/mathworks-ref-arch/matlab-dockerfile).**

## Supported Tags

| Tags         | MATLAB Version | Operating System | Base Image | Usage Notes |
| ------------ |:--------------:| ---------------- |----------- | ----------- |
|[`latest`, `r2022a`, `r2022a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2022a/ubuntu20.04/Dockerfile) | R2022a | Ubuntu 20.04 | ubuntu:20.04 | |
|[`r2022a-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2022a/ubi8/Dockerfile) | R2022a | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2021b`, `r2021b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2021b/ubuntu20.04/Dockerfile) | R2021b | Ubuntu 20.04 | ubuntu:20.04 | |
|[`r2021b-ubi8`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2021b/ubi8/Dockerfile) | R2021b | Red Hat UBI 8 | registry.access.redhat.​com/ubi8/ubi:latest | |
|[`r2021b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2021b/aws-batch/Dockerfile) | R2021b | Ubuntu 20.04 | nvidia/cuda:11.4.1-base-ubuntu20.04 | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|
|[`r2021a`, `r2021a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2021a/ubuntu20.04/Dockerfile) | R2021a | Ubuntu 20.04 | ubuntu:20.04 | |
|[`r2021a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2021a/aws-batch/Dockerfile) | R2021a | Ubuntu 20.04 | nvidia/cuda:11.2.2-base-ubuntu20.04 | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|
|[`r2020b`, `r2020b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2020b/ubuntu20.04/Dockerfile) | R2020b | Ubuntu 20.04 | ubuntu:20.04 | |
|[`r2020b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2020b/aws-batch/Dockerfile) | R2020b | Ubuntu 20.04 | nvidia/cuda:11.0-base-ubuntu20.04 | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|
|[`r2020a`, `r2020a-ubuntu18.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2020a/ubuntu18.04/Dockerfile) | R2020a | Ubuntu 18.04 | ubuntu:18.04 | |
|[`r2020a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2020a/aws-batch/Dockerfile) | R2020a | Ubuntu 18.04 | nvidia/cuda:10.1-base | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|
|[`r2019b`, `r2019b-ubuntu18.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2019b/ubuntu18.04/Dockerfile) | R2019b | Ubuntu 18.04 | ubuntu:18.04 | |
|[`r2019b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2019b/aws-batch/Dockerfile) | R2019b | Ubuntu 18.04 | nvidia/cuda:10.1-base | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|

## License
The license for this container is available [here](https://github.com/mathworks-ref-arch/container-images/blob/master/LICENSE.md).

## Security Reporting
To report suspected security issues, follow [these instructions](https://github.com/mathworks-ref-arch/container-images/blob/master/SECURITY.md).

## Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
