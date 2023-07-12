#!/bin/sh

 sudo git pull
 
 #sudo docker network rm flask
 # used to delete all images  --> sudo docker image prune -a
 sudo docker rmi $(sudo docker images -a --filter=dangling=true -q)
 
 cd services/cam && sh build.sh
 cd - 

 #cd services/web && sh build.sh 
 #cd - 
 cd services/ui  && sh build.sh 
 cd -

 cd services/crawler  && sh build.sh && 
 cd -

 sudo docker push zeroprg/flask-docker-swarm_cam:latest
 sudo docker push zeroprg/flask-docker-swarm_ui:latest
 #sudo docker push zeroprg/flask-docker-swarm_web:latest
 
 sudo docker service rm flask_cam flask_ui  # flask_web
 NETWORK_NAME="flask"

# Check if the network already exists
if sudo docker network ls --format '{{.Name}}' | grep -wq "$NETWORK_NAME"; then
    echo "Network $NETWORK_NAME already exists."
else
    echo "Creating network $NETWORK_NAME..."
    sudo docker network create "$NETWORK_NAME"
fi

 sudo docker stack deploy -c=$HOME/projects/flask-ai-classifier-docker-swarm/docker-compose-swarm.yml  --with-registry-auth $NETWORK_NAME

