docker build --platform linux/arm64 -t zeroprg/flask-docker-swarm_cam:amd64 .
docker build  -t zeroprg/flask-docker-swarm_cam:amd64 -f Docker.amd64 .
docker push zeroprg/flask-docker-swarm_cam:latest
docker push zeroprg/flask-docker-swarm_cam:amd64