Kafka Setup Guide
Introduction
This guide provides step-by-step instructions for setting up a single-node Kafka cluster on Ubuntu.

Prerequisites
Ubuntu 18.04 or later
Docker CE installed
Docker Compose installed
ZooKeeper Setup
Before setting up Kafka, we need to set up ZooKeeper, which is used by Kafka for coordination between nodes in a cluster.

Install ZooKeeper:
sudo apt-get update && sudo apt-get install -y zookeeperd
Start ZooKeeper:
sudo systemctl start zookeeper.service
Verify that ZooKeeper is running:
sudo systemctl status zookeeper.service
Kafka Setup
Now that we have set up ZooKeeper, we can move on to setting up Kafka.

Create a new directory for Kafka:
mkdir kafka && cd kafka
Create a 
docker-compose.yml
 file with the following contents:
version: '2'
services:
  kafka:
    image: wurstmeister/kafka:2.13-2.8.0
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:9092,OUTSIDE://${zookeeper_ip}:9092
      KAFKA_LISTENERS: INSIDE://0.0.0.0:9092,OUTSIDE://0.0.0.0:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
      KAFKA_ZOOKEEPER_CONNECT: ${zookeeper_ip}:2181
      KAFKA_CREATE_TOPICS: "multi_topic:3:1,preprocessed:1:1"
      KAFKA_LOG_RETENTION_HOURS: 24
      KAFKA_LOG_RETENTION_BYTES: 1048576
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
Note that the 
KAFKA_ADVERTISED_LISTENERS
 and 
KAFKA_LISTENERS
 environment variables have been set to allow connections from both inside and outside the Docker network. The 
kafka
 container will listen on port 9092 inside the network, and on port 9092 on the host machine (i.e., outside the network).

Also note that 
KAFKA_CREATE_TOPICS
 has been set to create two topics: 
multi_topic
, with three partitions and one replica, and 
preprocessed
, with one partition and one replica. 
KAFKA_LOG_RETENTION_HOURS
 has been set to 24 hours, and 
KAFKA_LOG_RETENTION_BYTES
 has been set to 1 MB for the 
preprocessed
 topic.

Start Kafka:
docker-compose up -d
Verify that Kafka is running:
docker-compose ps
Conclusion
You should now have a working Kafka cluster with ZooKeeper running on your Ubuntu machine. You can use the Kafka command-line tools or one of the many client libraries available to start sending and receiving messages.