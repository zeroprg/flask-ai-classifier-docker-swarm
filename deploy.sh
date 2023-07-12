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
 sudo docker network create flask 
 sudo docker stack deploy -c=$HOME/projects/flask-ai-classifier-docker-swarm/docker-compose-swarm.yml"  --with-registry-auth flask

