#Install qemu for multiarch build
docker run --privileged --rm tonistiigi/binfmt --install arm

# Build for ARM v7 from AMD64
docker build --platform=linux/arm/v7 -t zeroprg/flask-docker-swarm_ui:latest  .
# build for AMD64
docker build  -t zeroprg/flask-docker-swarm_ui:amd64  -f ./Docker.amd64 .