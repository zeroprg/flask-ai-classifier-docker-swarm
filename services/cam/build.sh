docker build --platform linux/arm32v8 --push -t zeroprg/flask-docker-swarm_cam:latest .
docker build  --push  -t zeroprg/flask-docker-swarm_cam:amd64 -f Docker.amd64 .