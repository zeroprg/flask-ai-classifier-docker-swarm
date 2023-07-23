#!/bin/bash

# This script run zookeeper and kafka server then creates (multiple) kafka topic(s) with retention policy 'compact'
# and one topic with retention policy 'delete' and maximum size of 1MB. Then run  web_ultralitics container  at the end
#
# Usage: ./run_kafka <kafka/zookeeper_ip>
#
# Example: ./run_kafka.sh 192.168.1.128

# Check if kafka/zookeeper IP is provided
if [ -z "$1" ]
  then
    echo "Error: No zookeeper IP provided. Exiting."
    exit 1
fi

host_ip="$1"

echo  "Running zookeeper ..."
sudo docker run -d --name zookeeper -e TZ=UTC -p 2181:2181 ubuntu/zookeeper
echo "Waiting for 5 seconds..."
sleep 5

echo "Running kafka ... (for additional arguments check: https://hub.docker.com/r/wurstmeister/kafka)"
docker run --name kafka -p 9092:9092 \
-e KAFKA_ZOOKEEPER_CONNECT=${host_ip}:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://${host_ip}:9092 \
-e KAFKA_ADVERTISED_HOST_NAME=${host_ip} \
-e KAFKA_DELETE_TOPIC_ENABLE=true \
-d wurstmeister/kafka:latest

echo "Waiting for 5 seconds..."
sleep 15


echo "Running topic 'preprocessed' creation ..."

sudo ./topic_create.sh ${host_ip}

#sudo docker exec -it kafka kafka-topics.sh --zookeeper  ${host_ip}:2181 \
#       --create --topic preprocessed --partitions 1 --replication-factor 1 \
#        --config cleanup.policy=delete

echo  "Running web_ultralitics ..."
sudo docker run --name web_ultralitics -e KAFKA_SERVER=${host_ip}:9092 -d zeroprg/flask-docker-swarm_web:latest python3 kafka_consumer.py
