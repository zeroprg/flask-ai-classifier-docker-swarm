#!/bin/bash

# Determine the platform
platform="$(uname -m)"
case "$platform" in
    x86_64)
        docker_platform="linux/amd64"
        tag_suffix="amd64"
        ;;
    armv7l)
        tag_suffix="arm32v7"
        ;;
    *)
        echo "Unsupported platform: $platform"
        exit 1
        ;;
esac

# Check if user is logged in to DockerHub
if ! docker info | grep -q Username; then
    echo "Please login to DockerHub first using 'docker login'"
    exit 1
fi

# Build Docker image
if [ "$platform" = "x86_64" ]; then
    docker build --platform linux/arm/v7 -t zeroprg/ultralitics:arm32v7 .
    #docker build --push -t zeroprg/ultralitics:amd64 -f Docker.amd64 .
else
    docker build -t "zeroprg/ultralitics:${tag_suffix}" .
fi

# Push the image to DockerHub
docker push "zeroprg/ultralitics:${tag_suffix}"

echo "Build and push for $platform completed!"