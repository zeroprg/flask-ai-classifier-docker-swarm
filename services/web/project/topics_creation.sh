#!/bin/bash

# This script creates multiple kafka topics with retention policy 'compact'
# and one topic with retention policy 'delete' and maximum size of 1MB.
#
# Usage: ./create_topics.sh <zookeeper_ip>
#
# Example: ./create_topics.sh 192.168.1.100

# Check if zookeeper IP is provided
if [ -z "$1" ]
  then
    echo "Error: No zookeeper IP provided. Exiting."
    exit 1
fi

zookeeper_ip="$1"

# Create topics with retention policy 'compact'
docker exec -it kafka kafka-topics.sh --zookeeper "${zookeeper_ip}:2181" --create --topic person --partitions 1 --replication-factor 1 --config cleanup.policy=compact
docker exec -it kafka kafka-topics.sh --zookeeper "${zookeeper_ip}:2181" --create --topic cow --partitions 1 --replication-factor 1 --config cleanup.policy=compact
docker exec -it kafka kafka-topics.sh --zookeeper "${zookeeper_ip}:2181" --create --topic dog --partitions 1 --replication-factor 1 --config cleanup.policy=compact

# Create topic with retention policy 'delete' and a maximum size of 1MB
docker exec -it kafka kafka-topics.sh --zookeeper "${zookeeper_ip}:2181" --create --topic preprocessed --partitions 1 --replication-factor 1 --config retention.ms=3600000 --config max.message.bytes=1000000 --config cleanup.policy=delete