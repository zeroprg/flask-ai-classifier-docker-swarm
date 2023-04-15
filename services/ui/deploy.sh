#!/bin/bash
sudo ./build.sh
docker stack deploy -c=../../docker-compose-swarm.yml flask
