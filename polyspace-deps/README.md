# Polyspace Dependencies

> :warning: **Starting in R2024a, the `polyspace-deps` repository will no longer receive updates or support.**
>
> To streamline the container workflows for Polyspace products, the libraries and other dependencies required to run Polyspace products in containers are now included in the `Dockerfile` of the corresponding products. To continue using Polyspace products in Docker containers, see:
>
>* [Polyspace Bug Finder and Code Prover Server](https://github.com/mathworks-ref-arch/polyspace-bug-finder-server-dockerfile)
>* [Polyspace Test](https://github.com/mathworks-ref-arch/polyspace-test-dockerfile)

This repository includes the libraries and other dependencies required to run the Polyspace Bug Finder&trade; Server&trade; and Polyspace Code Prover&trade; Server&trade; MathWorks&reg; products. These dependencies are installed during the build of a Polyspace Bug Finder/Code Prover Server container image.

To build and run a Polyspace Bug Finder Server and Polyspace Code Prover Server container, follow [these instructions](https://github.com/mathworks-ref-arch/polyspace-bug-finder-server-dockerfile) .

> **Note: The Polyspace dependencies do not include the Polyspace Bug Finder Server and Polyspace Code Prover Server products.**


## Supported Tags

| Tags         | Polyspace Version | Operating System | Base Image | Usage Notes |
| ------------ |:--------------:| ---------------- |----------- | ----------- |
|[`latest`, `r2023b`, `r2023b-ubuntu22.04`, `R2023b`, `R2023b-ubuntu22.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/polyspace-deps/r2023b/ubuntu22.04/Dockerfile) | R2023b | Ubuntu 22.04 | ubuntu:22.04 | |
|[`r2023a`, `r2023a-ubuntu20.04`, `R2023a`, `R2023a-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/polyspace-deps/r2023a/ubuntu20.04/Dockerfile) | R2023a | Ubuntu 20.04 | ubuntu:20.04 | |
|[`r2022b`, `r2022b-ubuntu20.04`, `R2022b`, `R2022b-ubuntu20.04`](https://github.com/mathworks-ref-arch/container-images/blob/main/polyspace-deps/r2022b/ubuntu20.04/Dockerfile) | R2022b | Ubuntu 20.04 | ubuntu:20.04 | |

## License
The license for this container is available [here](https://github.com/mathworks-ref-arch/container-images/blob/main/LICENSE.md).

## Security Reporting
To report suspected security issues, follow [these instructions](https://github.com/mathworks-ref-arch/container-images/blob/main/SECURITY.md).

## Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

----

Copyright 2022-2024 The MathWorks, Inc.

----