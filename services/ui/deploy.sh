sudo docker-compose build && sudo docker push zeroprg/flask-ai-classifier-docker-swarm_ui && cd ../.. &&  sudo docker stack deploy -c=docker-compose-swarm.yml flask
