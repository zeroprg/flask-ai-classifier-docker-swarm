from confluent_kafka import Consumer, KafkaError

def consume_messages():
    consumer_config = {
        'bootstrap.servers': 'your_kafka_broker_ip:9092',
        'group.id': 'your_consumer_group_id',
        'auto.offset.reset': 'earliest',  # Start consuming from the beginning of the topic
        'enable.auto.commit': False     # Disable auto-commit of offsets
    }

    consumer = Consumer(consumer_config)
    topic = 'preprocessed'

    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for messages, wait up to 1 second if no messages are available

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f'Reached end of partition for topic {msg.topic()}')
                else:
                    print(f'Error while consuming message: {msg.error()}')
            else:
                print(f'Received message key: {msg.key().decode("utf-8")}')

            # Manually commit the offset to mark the message as processed
            consumer.commit(asynchronous=False)

    except KeyboardInterrupt:
        print('Consumer interrupted.')
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_messages()
