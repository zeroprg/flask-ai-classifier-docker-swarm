from confluent_kafka import Consumer, KafkaException

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
group_id = 'my-consumer-group'
topic = 'my-topic'

# Create consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

# Create Kafka consumer
consumer = Consumer(consumer_config)

# Subscribe to the topic
consumer.subscribe([topic])

# Consume messages from the topic
try:
    while True:
        # Poll for new messages
        message = consumer.poll(timeout=1.0)

        if message is None:
            continue

        if message.error():
            if message.error().code() == KafkaException._PARTITION_EOF:
                # End of partition, continue to next message
                continue
            else:
                # Handle error
                print(f"Error occurred: {message.error().str()}")
                break

        # Process the received message
        key = message.key()
        value = message.value()
        topic = message.topic()
        partition = message.partition()
        offset = message.offset()

        print(f"Received message: key={key}, value={value}, topic={topic}, partition={partition}, offset={offset}")

        # Commit the offset to mark the message as processed
        consumer.commit(message)

except KeyboardInterrupt:
    # Close the consumer on interrupt
    consumer.close()
