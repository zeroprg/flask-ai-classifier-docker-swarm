from pykafka import KafkaClient

def consume_messages():
    client = KafkaClient(hosts='192.168.0.128:9092')
    topic = client.topics[b'preprocessed']
    # Specify the consumer group ID here
    consumer_group_id = 'my-consumer-group'
    consumer = topic.get_simple_consumer( consumer_group=consumer_group_id, reset_offset_on_start=True)
    while True:
        try:
            for msg in consumer:
                if msg is not None:
                    partition_key = msg.partition_key  # Access the partition key of the message
                    print(f'Received message with partition key "{partition_key}"')
                    print(f'Received message length : {len(msg.value)}')
                    consumer.commit_offsets()  # Manually commit the offset to mark the message as processed

        except KeyboardInterrupt:
            print('Consumer interrupted.')
        finally:
            consumer.stop()

if __name__ == '__main__':
    consume_messages()
