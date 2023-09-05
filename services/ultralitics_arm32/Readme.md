Webultralitics ARMv7 Docker Image
=================================

This repository provides a Dockerfile to build a Webultralitics YOLOv5 image compatible with the ARMv7 (or arm32v7 in Docker terms) architecture.

Prerequisites
-------------

- Docker 19.03 or newer.

Quick Start
-----------

### Building the Docker Image

#### On Linux:

1. Prepare the environment for multi-architecture builds:
`chmod +x prepare_buildx.sh ./prepare_buildx.sh`

2. Build the Docker image:

`docker buildx build --platform linux/arm/v7 -t webultralitics:arm32v7 .`

#### On Windows:

1. Open PowerShell as Administrator.
2. Navigate to the directory containing your Dockerfile and scripts.
3. Prepare the environment for multi-architecture builds:

`.\prepare_buildx.ps1`

4. Build the Docker image:

Using Webultralitics
--------------------

After building the Docker image, you can run Webultralitics using:

`docker run -it --rm ultralitics:arm32v7`

For comprehensive details on using Webultralitics, refer to the [Webultralitics YOLOv5 official documentation](https://github.com/ultralytics/yolov5).

Notes
-----

- This Docker image is optimized for ARMv7 architecture, and it may not be the best fit for other architectures.
- Ensure you've tested the image on your target hardware before deploying it to production environments.

