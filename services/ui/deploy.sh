git pull
sudo docker-compose build
sudo docker push zeroprg/flask-ai-classifier-docker-swarm_ui
sudo docker stack deploy -c=../../docker-compose-swarm.yml flask
