sudo docker exec -it kafka kafka-topics.sh --bootstrap_server localhost:9092 --create --topic preprocessed --partitions 1 --replication-factor 1 --config retention.ms=3600000 --config max.message.bytes=5000000 --config cleanup.policy=delete 
sudo docker run --name web_ultralitics -e KAFKA_SERVER=loclhost:9092 -d zeroprg/flask-docker-swarm_web:latest
#sudo docker run --name web_ultralitics2 --gpus all -d zeroprg/flask-docker-swarm_web:amd64
