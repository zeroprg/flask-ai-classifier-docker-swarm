from confluent_kafka import Consumer
from PIL import Image

bootstrap_servers = 'your_kafka_brokers'
topic = 'postprocessing'
group_id = 'your_consumer_group'

# Create consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

# Create Kafka consumer
consumer = Consumer(consumer_config)
consumer.subscribe([topic])

def read_images_by_key_and_time_range(start_time_ms, end_time_ms, key):
    # Convert start and end time to seconds
    start_time_sec = start_time_ms / 1000
    end_time_sec = end_time_ms / 1000

    # Poll for new messages
    while True:
        message = consumer.poll(timeout=1.0)

        if message is None:
            continue

        if message.error():
            print(f"Error occurred: {message.error().str()}")
            continue

        # Process the received message
        message_time_sec = message.timestamp()[1] / 1000

        if start_time_sec <= message_time_sec <= end_time_sec and message.key() == key.encode('utf-8'):
            image_data = message.value()
            image = Image.open(image_data)
            image.show()

        # Commit the offset to mark the message as processed
        consumer.commit(message)

        if message_time_sec > end_time_sec:
            break

# Example usage
if __name__ == '__main__':
    start_time_ms = ...  # Specify the start time in milliseconds
    end_time_ms = ...    # Specify the end time in milliseconds
    key = 'your_key'

    read_images_by_key_and_time_range(start_time_ms, end_time_ms, key)
