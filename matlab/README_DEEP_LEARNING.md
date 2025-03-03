# MATLAB Deep Learning Docker Container

Speed up your deep learning applications by training neural networks in the MATLAB&reg; Deep Learning Container. This container is designed to take full advantage of high-performance NVIDIA&reg; GPUs. It provides a simple and flexible solution to use MATLAB for deep learning workflows in cloud environments such as AWS&reg; or Microsoft&reg; Azure&reg;.

## Supported tags

| Tags | MATLAB Version | Operating System | Base Image |
| ---- |:--------------:| ---------------- | ---------- |
| `latest`, `R2024b`, `r2024b` | R2024b | Ubuntu&reg; 22.04 | ubuntu:22.04 |
| `R2024a`, `r2024a` | R2024a | Ubuntu 22.04 | ubuntu:22.04 |
| `R2023b`, `r2023b` | R2023b | Ubuntu 22.04 | ubuntu:22.04 |
| `R2023a`, `r2023a` | R2023a | Ubuntu 20.04 | ubuntu:20.04 |
| `R2022b`, `r2022b` | R2022b | Ubuntu 20.04 | ubuntu:20.04 |
| `R2022a`, `r2022a` | R2022a | Ubuntu 20.04 | ubuntu:20.04 |
| `R2021b`, `r2021b` | R2021b | Ubuntu 20.04 | ubuntu:20.04 |

## Quick Launch Instructions
This section describes an example workflow to pull the R2024b MATLAB Deep Learning image and launch an interactive MATLAB session from the image.

To pull the R2024b MATLAB image to your machine, execute:
```console
docker pull mathworks/matlab-deep-learning:r2024b
```

To launch the container with the `-browser` option, execute:
```console
docker run -it --rm -p 8888:8888 --shm-size=512M mathworks/matlab-deep-learning:r2024b -browser
```

Executing this command will display a URL on which you can access MATLAB, for example:
```console
http://localhost:8888/index.html
```

For more information on running the container, see the section on [How to use this image](#How-to-use-this-image).

## What is MATLAB?
[MATLAB](https://www.mathworks.com/products/matlab.html) is a programming platform designed for engineers and scientists. It combines a desktop environment tuned for iterative analysis and design processes with a programming language that expresses matrix and array mathematics directly. For more information, [click this link to access our website](https://www.mathworks.com/discovery/what-is-matlab.html).

The MATLAB Deep Learning Container provides algorithms, pretrained models, and apps to create, train, visualize, and optimize deep neural networks. You can also access tools for image and signal processing, text analytics, and automatically generating C and CUDA&reg; code for deployment on NVIDIA&reg; GPUs in data centers and embedded systems. Specifically, this container provides an Ubuntu-based image with an installation of MATLAB and the following toolboxes:

* Computer Vision Toolbox&trade;
* Deep Learning Toolbox&trade;
* GPU Coder&trade;
* Image Processing Toolbox&trade;
* MATLAB Coder&trade;
* Parallel Computing Toolbox&trade;
* Signal Processing Toolbox&trade;
* Statistics and Machine Learning Toolbox&trade;
* Text Analytics Toolbox&trade;

and the following Support Packages:

* Deep Learning Toolbox Converter for TensorFlow Models
* Deep Learning Toolbox Converter for ONXX Models Format
* Deep Learning Toolbox Importer for Caffe Models
* Deep Learning Toolbox Model for AlexNet Network
* Deep Learning Toolbox Model for GoogLeNet Network
* Deep Learning Toolbox Model for Inception-v3 Network
* Deep Learning Toolbox Model for Inception-ResNet-v2 Network
* Deep Learning Toolbox Model for ResNet-18 Network
* Deep Learning Toolbox Model for ResNet-50 Network
* Deep Learning Toolbox Model for ResNet-101 Network
* GPU Coder Interface for Deep Learning Libraries
* MATLAB Coder Interface for Deep Learning Libraries
* (since R2023a) Deep Learning Toolbox Verification Library

## Configure your license
To use the MATLAB Deep Learning Container, you need a license for the MathWorks&reg; products in the container.

To train deep learning models, you need a license for MATLAB, Deep Learning and Parallel Computing toolboxes. If you are licensed to use the additional products in the container, its functionality is extended.

On public cloud instances like Amazon EC2&reg;, you can use a license that is enabled for cloud use. For on-premise DGX use, you can use a concurrent license by specifying the location of the network license manager when you run the container. Individual and Campus-Wide licenses are already configured for cloud use. For other license types, contact your license administrator. You can identify your license type and administrator by viewing your [MathWorks Account](https://www.mathworks.com/login). Administrators can consult [Administer Network Licenses](https://www.mathworks.com/help/install/administer-network-licenses.html).

## How to use this image

This section describes the different options you can use to run the container, depending on your use case. Some options allow you to interact with MATLAB via the command line interface while others let you interact with the MATLAB desktop.

### Run MATLAB with GPUs on your host machine

Before you start the container, check that your graphics driver is up to date. See [MATLAB GPU Computing Requirements](https://www.mathworks.com/help/parallel-computing/gpu-computing-requirements.html) for details.

To start the container and run MATLAB with GPUs on your host machine, execute:

```console
$ docker run --gpus all -it --rm --shm-size=512M mathworks/matlab-deep-learning:r2024b
```

By default, a container does not have access to hardware resources of its host. To enable the container to access the GPUs of the host system, use the `--gpus` flag when you execute the `docker run` command. Set this flag to `all` if you want the container to have access to all the GPUs of the host machine.

For more information, see [Access an NVIDIA GPU](https://docs.docker.com/engine/reference/commandline/container_run/#gpus).

### Run MATLAB in an interactive command prompt

To start the container and run MATLAB in an interactive command prompt, execute:

```console
$ docker run -it --rm mathworks/matlab-deep-learning:r2024b
```

### Run MATLAB non-interactively in batch mode
To start the container and run the MATLAB command `RAND`, execute:
```console
$ docker run --rm -e MLM_LICENSE_FILE=27000@MyLicenseServer mathworks/matlab-deep-learning:r2024b -batch rand
```
where you must replace `27000@MyLicenseServer` with the correct port number and DNS address for your network license manager.

Alternatively, if your system administrator provides you with a license file, you can mount the license file to the container and point `MLM_LICENSE_FILE` to the license file path in the container. For example, to start the container and run the MATLAB command `RAND` with a license file, execute:
```console
$ docker run --rm -v /path/to/local/license/file:/licenses/license.lic -e MLM_LICENSE_FILE=/licenses/license.lic mathworks/matlab-deep-learning:r2024b -batch rand
```

If a valid license file is provided, the container runs the command `RAND` in MATLAB and exits. For more information on using the network license manager, see [Use the Network License Manager](https://github.com/mathworks-ref-arch/matlab-dockerfile#use-the-network-license-manager).

### Run MATLAB and interact with it via a web browser

To start the container, execute:
```console
$ docker run -it --rm -p 8888:8888 --shm-size=512M mathworks/matlab:r2024b -browser
```

Running the above command prints text to your terminal containing the URL to access MATLAB. For example:

```console
MATLAB can be accessed at:
http://localhost:8888/index.html
```
Enter the provided URL into a web browser. If prompted to do so, enter credentials for a MathWorks account associated with a MATLAB license.
If you are using a network license manager, change to the Network License Manager tab and enter the license server address instead. After you provide your license information, a MATLAB session will start in the browser (this may take several minutes).

To modify the behavior of MATLAB when launched with `-browser` flag, pass environment variables to the `docker run` command. For more information, see [Advanced-Usage.md](https://github.com/mathworks/matlab-proxy/blob/main/Advanced-Usage.md).

Some browsers may not support this workflow. For more information, see [Cloud Solutions Browser Requirements](https://www.mathworks.com/support/requirements/browser-requirements.html).

**NOTE:** The `-browser` flag is supported by Docker&reg; images starting from MATLAB `R2022a`.
To access MATLAB in a web browser in custom Docker images with MATLAB or older MATLAB Docker images, for example `R2021b`, see [examples](https://github.com/mathworks/matlab-proxy/blob/main/examples/Dockerfile).


### Run MATLAB in desktop mode and interact with it via VNC

To start the MATLAB desktop, execute:

```console
$ docker run -it --rm -p 5901:5901 -p 6080:6080 --shm-size=512M mathworks/matlab-deep-learning:r2024b -vnc
```

To connect to the MATLAB desktop, either:

1. Point a browser to port 6080 of the Docker host machine running this container (`http://hostname:6080`)
2. Use a VNC client to connect to display 1 of the Docker host machine (`hostname:1`)

The VNC password is `matlab` by default. Use the `PASSWORD` environment variable to change it. If you are using a cloud service provider or your host or client machines are protected by a firewall, you must set up SSH tunnels between your client machine and the Docker host to access the container desktop. For instructions, see the [Create Encrypted Connection to Remote Applications and Containers](https://www.mathworks.com/help/cloudcenter/ug/create-encrypted-connection-to-remote-applications-and-containers.html).

### Run MATLAB desktop using X11

To start the container and run MATLAB desktop using X11, execute:

```console
$ xhost +
$ docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro --shm-size=512M mathworks/matlab-deep-learning:r2024b
```

The MATLAB desktop window will open on your machine. Note that the command above works only on a Linux operating system with ```X11``` and its dependencies installed.


### Run MATLAB with startup options

To override the default behavior of the container and run MATLAB with any set of arguments, such as `-logfile`, execute:

```console
$ docker run -it --rm mathworks/matlab-deep-learning:r2024b -logfile "logfilename.log"
```

## Environment variables
When executing the command `docker run` you can specify environment variables using the option `-e`. This section describes all the environment variables that you can specify.

 #### ```MLM_LICENSE_FILE ```
Use this environment variable when you want to use either a license file or a network license manager to license MATLAB.

<i>Example:</i>

`docker run -it --rm -e MLM_LICENSE_FILE=27000@MyLicenseServer mathworks/matlab-deep-learning:r2024b`
<br />

`docker run -it --rm -e MLM_LICENSE_FILE=/license.dat mathworks/matlab-deep-learning:r2024b`

#### ```PROXY_SETTINGS```
Use this environment variable when you want to use a proxy server to connect to the MathWorks licensing servers.

<i>Example:</i>

`docker run -it --rm -e PROXY_SETTINGS=<proxy-server-address> mathworks/matlab-deep-learning:r2024b`

You can specify the proxy server address using any of the following forms:

* `hostname:12345`
* `shorthostname:12345`
* `http://hostname:12345`
* `http://username:password@hostname:12345`
* `IPaddress:12345`

where `hostname` is the fully qualified domain name, `shorthostname` is the relative domain name, and 12345 is the port number.

#### ```PASSWORD```
Use this environment variable when you want to change the password used to access the VNC server.

<i>Example:</i>

`docker run -it --rm -e PASSWORD=ILoveMATLAB -p 5901:5901 -p 6080:6080 --shm-size=512M mathworks/matlab-deep-learning:r2024b -vnc`

### Install updates, toolboxes, add-ons in the container and save changes

You can install the latest MATLAB updates or install additional toolboxes and add-ons in this container. For more information, see [Install Updates, Toolboxes, Support Packages, and Add-Ons in Containers](https://www.mathworks.com/help/cloudcenter/ug/install-updates-toolboxes-support-packages-and-add-ons-in-containers.html).

## Security reporting
Follow these instructions to [report suspected security issues](https://github.com/mathworks-ref-arch/container-images/blob/master/SECURITY.md).

## Additional information
This container includes commercial software products of The MathWorks, Inc. ("MathWorks Programs") and related materials. MathWorks Programs are licensed under the MathWorks Software License Agreement, available in the MATLAB installation in this container. Related materials in this container are licensed under separate licenses which can be found in their respective folders.

To learn more about MATLAB containers, see [MATLAB Container on Docker Hub](https://www.mathworks.com/help/cloudcenter/ug/matlab-container-on-docker-hub.html).

To see the source files used to build this Docker image, see the [MATLAB Container Images on GitHub](https://github.com/mathworks-ref-arch/container-images/tree/main/matlab).

To provide suggestions for additional features or capabilities, [contact us](https://www.mathworks.com/solutions/cloud.html).

## Technical support
If you require assistance or have a request for additional features or capabilities, contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

Copyright 2021-2025 The MathWorks, Inc.
