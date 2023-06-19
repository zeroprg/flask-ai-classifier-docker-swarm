docker run -d --name=kafka -p 9092:9092 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_CREATE_TOPICS="my-topic:1:1:compact" confluentinc/cp-kafka:latest
