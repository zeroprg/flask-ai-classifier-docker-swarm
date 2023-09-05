docker buildx create --use
docker buildx build  --push --platform linux/arm/v7 -t zeroprg/flask-docker-swarm_web:latest .
docker build --push -t zeroprg/flask-docker-swarm_web:amd64 -f Docker.amd64 .
