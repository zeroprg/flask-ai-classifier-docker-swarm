#!/bin/bash

# Ensure user is running Docker 19.03 or newer
DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
if [[ $DOCKER_VERSION < "19.03" ]]; then
    echo "You need Docker version 19.03 or newer"
    exit 1
fi

# Enable experimental CLI features
export DOCKER_CLI_EXPERIMENTAL=enabled

# Install docker-buildx if not already installed
if ! docker buildx inspect default > /dev/null 2>&1; then
    docker plugin install docker/cli-plugin/docker-buildx
fi

# Create and bootstrap the builder
BUILDER_NAME=mybuilder

docker buildx create --name $BUILDER_NAME --use
docker buildx inspect $BUILDER_NAME --bootstrap

echo "Buildx preparation completed."
