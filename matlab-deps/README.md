# MATLAB Dependencies

This container includes the dependencies required to run MATLAB®, Simulink®, and other MathWorks products.

**Note: This container does not include MATLAB.  To build a MATLAB container, follow [these instructions](https://github.com/mathworks-ref-arch/matlab-dockerfile).**

## Supported Tags

| Tags         | MATLAB Version | Operating System | Base Image | Usage Notes |
| ------------ |:--------------:| ---------------- |----------- | ----------- |
|[`latest`, `r2020a`, `r2020a-ubuntu18.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2020a/ubuntu18.04/Dockerfile) | R2020a | Ubuntu 18.04 | ubuntu:18.04 | |
|[`r2020a-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2020a/aws-batch/Dockerfile) | R2020a | Ubuntu 18.04 | nvidia/cuda:10.1-base | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|
|[`r2019b`, `r2019b-ubuntu18.04`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2019b/ubuntu18.04/Dockerfile) | R2019b | Ubuntu 18.04 | ubuntu:18.04 | |
|[`r2019b-aws-batch`](https://github.com/mathworks-ref-arch/container-images/blob/master/matlab-deps/r2019b/aws-batch/Dockerfile) | R2019b | Ubuntu 18.04 | nvidia/cuda:10.1-base | For use with [MATLAB® Parallel Server™ with AWS® Batch](https://github.com/mathworks-ref-arch/matlab-parallel-server-with-aws-batch)|

## License
The license for this container is available [here](https://github.com/mathworks-ref-arch/container-images/blob/master/LICENSE.md).

## Security Reporting
To report suspected security issues, follow [these instructions](https://github.com/mathworks-ref-arch/container-images/blob/master/SECURITY.md).

## Technical Support
Email: `cloud-support@mathworks.com`
