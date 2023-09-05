docker buildx create --use
docker build --output=type=image,push=true,format=docker --platform linux/arm/v7 -t zeroprg/flask-docker-swarm_web:latest .
docker build --push -t zeroprg/flask-docker-swarm_web:amd64 -f Docker.amd64 .
