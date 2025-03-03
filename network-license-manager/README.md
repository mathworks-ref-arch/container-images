# Docker Container for Network License Manager

This repository allows you to install and start a license server with a single command using a Docker&reg; container image and Docker Compose file for Network License Manager.

### Requirements
* Docker (with Docker Engine 18.06.0 or higher)
* Linux&reg; host
* Network License File for the Linux host

## Run Network License Server Instance

### Get Sources

Download this container image either by cloning or downloading this repository from GitHub&reg;,
and navigate to the `network-license-manager` folder.
```bash
git clone https://github.com/mathworks-ref-arch/container-images.git
cd container-images/network-license-manager
```

### Provide License File

Copy your [network license file](https://www.mathworks.com/help/install/ug/network-license-files.html) to the `licenses` folder within the `network-license-manager` folder of the repository as `license.dat`. Network License Manager will use this license.

For more information about license files, see [support article](https://www.mathworks.com/matlabcentral/answers/116637-what-are-the-differences-between-the-license-lic-license-dat-network-lic-and-license_info-xml-lic#answer_124791).

### Run Container Image

Run the container image with Docker Compose. The container image must be run on the machine for which the network license file is activated.
```bash
docker compose up
```

This command starts the license server. Logs are written to the terminal as well as to the `logs` folder within the `network-license-manager` folder of the repository.

To stop the container, either press `Ctrl+C` or use this command.
```bash
docker compose down
```

#### Network License Manager Port Lifetime

If you stop and restart the container within a short time (one to two minutes), you may see the following error from the Network License Manager: "Failed to open the TCP port number in the license". This occurs because the operating system may keep the required port temporarily open. To resolve this issue, wait a short time (one to two minutes) and restart the container.

## Technical Support
If you require assistance or have a request for additional features or capabilities, contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html) with the relevant `logs`.

----

Copyright 2024-2025 The MathWorks, Inc.

----