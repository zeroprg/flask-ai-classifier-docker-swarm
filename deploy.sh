#!/bin/bash

 git pull
 sudo docker-compose build
 sudo docker push zeroprg/flask-docker-swarm_cam:latest
 sudo docker push zeroprg/flask-docker-swarm_web:latest
 sudo docker stack deploy -c=docker-compose-swarm.yml flask
 
