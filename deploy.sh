#!/bin/sh

 git pull
 cd services/cam && sh build.sh
 cd - && cd services/web && sh build.sh && cd ../..
 sudo docker image prune -a
 sudo docker service rm flask_web flask_cam
 sudo docker push zeroprg/flask-docker-swarm_cam:latest
 sudo docker push zeroprg/flask-docker-swarm_web:latest
 sudo docker stack deploy -c=docker-compose-swarm.yml flask
 
