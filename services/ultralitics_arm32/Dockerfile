# Ultralytics YOLO 🚀, AGPL-3.0 license
# Builds ultralytics/ultralytics:latest-arm32v7 image on DockerHub https://hub.docker.com/r/ultralytics/ultralytics
# Image is arm32v7-compatible for Raspberry Pi and other 32-bit ARM architectures

# Start FROM Ubuntu image https://hub.docker.com/_/ubuntu
FROM arm32v7/ubuntu:22.04

# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf https://ultralytics.com/assets/Arial.Unicode.ttf /root/.config/Ultralytics/

# Install linux packages
# g++ required to build 'tflite_support' and 'lap' packages, libusb-1.0-0 required for 'tflite_support' package
RUN apt update \
    && apt install --no-install-recommends -y python3-pip git zip curl htop gcc libgl1-mesa-glx libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0
# RUN alias python=python3

# Create working directory
WORKDIR /usr/src/ultralytics

# Copy contents
# COPY . /usr/src/ultralytics  # git permission issues inside container
RUN git clone https://github.com/ultralytics/ultralytics -b main /usr/src/ultralytics
ADD https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt /usr/src/ultralytics/

# Install pip packages
# Install thop and other required packages
#used only for FLOP calculations
#RUN python3 -m pip install --upgrade pip wheel thop


# Creates a symbolic link to make 'python' point to 'python3'
RUN ln -sf /usr/bin/python3 /usr/bin/python


# Usage Examples -------------------------------------------------------------------------------------------------------

# Build and Push
# t=ultralytics/ultralytics:latest-arm32v7 && sudo docker build --platform linux/arm/v7 -f docker/Dockerfile-arm32v7 -t $t . && sudo docker push $t

# Run
# t=ultralytics/ultralytics:latest-arm32v7 && sudo docker run -it --ipc=host $t

# Pull and Run
# t=ultralytics/ultralytics:latest-arm32v7 && sudo docker pull $t && sudo docker run -it --ipc=host $t

# Pull and Run with local volume mounted
# t=ultralytics/ultralytics:latest-arm32v7 && sudo docker pull $t && sudo docker run -it --ipc=host -v "$(pwd)"/datasets:/usr/src/datasets $t
