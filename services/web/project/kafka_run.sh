docker run --name kafka -p 9092:9092 \
-e KAFKA_ZOOKEEPER_CONNECT=$zookeeper_ip:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://$zookeeper_ip:9092 \
-e KAFKA_ADVERTISED_HOST_NAME=$zookeeper_ip \
-d wurstmeister/kafka:latest