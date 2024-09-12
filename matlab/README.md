# MATLAB Docker Container

Access MATLAB&reg; in the cloud or in server environments by using the prebuilt MATLAB container. This container also allows you to interact with MATLAB using your browser and Virtual Network Computing (VNC).


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
| `R2021a`, `r2021a` | R2021a | Ubuntu 20.04 | ubuntu:20.04 |
| `R2020b`, `r2020b` | R2020b | Ubuntu 20.04 | ubuntu:20.04 |

## Quick Launch Instructions
This section describes an example workflow to pull the R2024b MATLAB image and launch an interactive MATLAB session from the image.

To pull the R2024b MATLAB image to your machine, execute:
```console
docker pull mathworks/matlab:r2024b
```

To launch the container with the `-browser` option, execute:
```console
docker run -it --rm -p 8888:8888 --shm-size=512M mathworks/matlab:r2024b -browser
```
You will be provided with a URL for accessing MATLAB in a web browser.

For more information on running the container, see the section on [How to use this image](#How-to-use-this-image).

## What is MATLAB?

[MATLAB](https://www.mathworks.com/products/matlab.html) is a programming platform designed for engineers and scientists. It combines a desktop environment tuned for iterative analysis and design processes with a programming language that expresses matrix and array mathematics directly. For more information, [click this link to access our website](https://www.mathworks.com/discovery/what-is-matlab.html).

The MATLAB Container provides an Ubuntu based image with a MATLAB installation.

## Configure your license

To run this container your license must be configured for cloud use. Individual and Campus-Wide licenses are already configured for cloud use. For other license types, contact your license administrator. You can identify your license type and administrator by viewing your [MathWorks Account](https://www.mathworks.com/login). Administrators can consult [Administer Network Licenses](https://www.mathworks.com/help/install/administer-network-licenses.html). If you don't have a MATLAB license, you can get a trial license at [MATLAB Trial for Docker](https://www.mathworks.com/campaigns/products/trials/targeted/dkr.html).

## How to use this image

This section describes the different options you can use to run the container, depending on your use case. Some options allow you to interact with MATLAB via the command line interface while others let you interact with the MATLAB desktop.

### Run MATLAB in an interactive command prompt

To start the container and run MATLAB in an interactive command prompt, execute:

```console
$ docker run -it --rm --shm-size=512M mathworks/matlab:r2024b
```

### Run MATLAB non-interactively in batch mode

To start the container and run the MATLAB command `RAND`, execute:
```console
$ docker run --rm -e MLM_LICENSE_FILE=27000@MyLicenseServer mathworks/matlab:r2024b -batch rand
```
where you must replace `27000@MyLicenseServer` with the correct port number and DNS address for your network license manager.

Alternatively, if your system administrator provides you with a license file, you can mount the license file to the container and point `MLM_LICENSE_FILE` to the license file path in the container. For example, to start the container and run the MATLAB command `RAND` with a license file, execute:
```console
$ docker run --rm -v /path/to/local/license/file:/licenses/license.lic -e MLM_LICENSE_FILE=/licenses/license.lic mathworks/matlab:r2024b -batch rand
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
Enter the provided URL into a web browser. If prompted to do so, enter credentials for a MathWorks&reg; account associated with a MATLAB license.
If you are using a network license manager, change to the Network License Manager tab and enter the license server address instead. After you provide your license information, a MATLAB session will start in the browser (this may take several minutes).

To modify the behaviour of MATLAB when launched with `-browser` flag, pass environment variables to the `docker run` command. For more information, see [Advanced-Usage.md](https://github.com/mathworks/matlab-proxy/blob/main/Advanced-Usage.md).

Some browsers may not support this workflow. For more information, see [Cloud Solutions Browser Requirements](https://www.mathworks.com/support/requirements/browser-requirements.html).

**NOTE:** The `-browser` flag is supported by Docker&reg; images starting from MATLAB `R2022a`.
To access MATLAB in a web browser in custom Docker images or older MATLAB Docker images, for example `R2021b`, see [examples](https://github.com/mathworks/matlab-proxy/blob/main/examples/Dockerfile).

### Run MATLAB in desktop mode and interact with it via VNC

To start the MATLAB desktop, execute:

```console
$ docker run -it --rm -p 5901:5901 -p 6080:6080 --shm-size=512M mathworks/matlab:r2024b -vnc
```

To connect to the MATLAB desktop, either:

1. Point a browser to port 6080 of the Docker host machine running this container (`http://hostname:6080`)
2. Use a VNC client to connect to display 1 of the Docker host machine (`hostname:1`)

The VNC password is `matlab` by default. Use the `PASSWORD` environment variable to change it.

### Run MATLAB desktop using X11

To start the container and run MATLAB desktop using `X11`, execute:

```console
$ xhost +
$ docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro --shm-size=512M mathworks/matlab:r2024b
```

The MATLAB desktop window will open on your machine.
Note that the command above works only on a Linux&reg; operating system with `X11` and its dependencies installed.

### Run MATLAB with startup options

To override the default behavior of the container and run MATLAB with any set of arguments, such as `-logfile`, execute:

```console
$ docker run -it --rm --shm-size=512M mathworks/matlab:r2024b -logfile "logfilename.log"
```

### Environment variables
When executing the command `docker run` you can specify environment variables using the option `-e`. This section describes all the environment variables that you can specify.

#### `MLM_LICENSE_FILE`

Use this environment variable when you want to use either a license file or a network license manager to license MATLAB.

<i>Example:</i>

`docker run -it --rm -e MLM_LICENSE_FILE=27000@MyLicenseServer --shm-size=512M mathworks/matlab:r2024b`
<br />

`docker run -it --rm -e MLM_LICENSE_FILE=/license.dat --shm-size=512M mathworks/matlab:r2024b`

#### `PROXY_SETTINGS`

Use this environment variable when you want to use a proxy server to connect to the MathWorks licensing servers.

<i>Example:</i>

`docker run -it --rm -e PROXY_SETTINGS=<proxy-server-address> --shm-size=512M mathworks/matlab:r2024b`

You can specify the proxy server address using any of the following forms:

- `hostname:12345`
- `shorthostname:12345`
- `http://hostname:12345`
- `http://username:password@hostname:12345`
- `IPaddress:12345`

where `hostname` is the fully qualified domain name, `shorthostname` is the relative domain name, and 12345 is the port number.

#### `PASSWORD`

Use this environment variable when you want to change the password used to access the VNC server.

<i>Example:</i>

`docker run -it --rm -e PASSWORD=ILoveMATLAB -p 5901:5901 -p 6080:6080 --shm-size=512M mathworks/matlab:r2024b -vnc`

### Create a custom Docker image from the MATLAB container base image

Create a file named `Dockerfile` with the following content:

```dockerfile
## Build from the MATLAB base image
FROM mathworks/matlab:r2024b

## Copy your script/function to be executed.
COPY myscript.m ./

## Start MATLAB in batch mode and execute your script/function.
CMD ["matlab","-batch","myscript"]
```

You can then build and run the Docker image:

```console
$ docker build -t my-matlab-container .
$ docker run -it --rm --shm-size=512M my-matlab-container
```

### Install updates, toolboxes, add-ons in the container and save changes

You can install the latest MATLAB updates or install additional toolboxes and add-ons in this container. For more information, see [Install Updates, Toolboxes, Support Packages, and Add-Ons in Containers](https://www.mathworks.com/help/cloudcenter/ug/install-updates-toolboxes-support-packages-and-add-ons-in-containers.html).

## Security reporting
Follow these instructions to [report suspected security issues](https://github.com/mathworks-ref-arch/container-images/blob/master/SECURITY.md).

## Additional information
This container includes commercial software products of The MathWorks, Inc. ("MathWorks Programs") and related materials. MathWorks Programs are licensed under the MathWorks Software License Agreement, available in the MATLAB installation in this container. Related materials in this container are licensed under separate licenses which can be found in their respective folders.

To learn more about MATLAB containers, see [MATLAB Container on Docker Hub](https://www.mathworks.com/help/cloudcenter/ug/matlab-container-on-docker-hub.html).

To see the source files used to build this Docker image, see the [MATLAB Container Images on GitHub](https://github.com/mathworks-ref-arch/container-images/matlab-dockerhub).

To provide suggestions for additional features or capabilities, [contact us](https://www.mathworks.com/solutions/cloud.html).

## Technical support
If you require assistance or have a request for additional features or capabilities, contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

Copyright 2020-2024 The MathWorks, Inc.