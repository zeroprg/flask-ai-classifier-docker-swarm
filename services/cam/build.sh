# Check the architecture and set the ARCH variable accordingly
if [ "$(uname -m)" = "x86_64" ]; then
  ARCH="amd64"  
  docker buildx build --platform linux/arm --push -t zeroprg/flask-docker-swarm_cam:latest .
  docker build  --push  -t zeroprg/flask-docker-swarm_cam:amd64 -f Docker.amd64 .
else
  ARCH="arm"
  docker build  -t zeroprg/flask-docker-swarm_cam:latest .
fi
