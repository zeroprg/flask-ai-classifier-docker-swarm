docker build --platform linux/arm64 -t zeroprg/flask-docker-swarm_web:amd64 .
docker build  -t zeroprg/flask-docker-swarm_web:amd64 -f Docker.amd64 .
docker push zeroprg/flask-docker-swarm_web:latest
docker push zeroprg/flask-docker-swarm_web:amd64
