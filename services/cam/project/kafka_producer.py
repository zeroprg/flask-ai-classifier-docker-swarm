from confluent_kafka import Producer
import struct
from base64 import b64encode
from PIL import Image
import zlib
from io import BytesIO
import uuid

from project.config import  ProductionConfig as prod

# Kafka broker configuration
bootstrap_servers = prod.KAFKA_SERVER #'172.29.208.1:9092'
topic = prod.KAFKA_PREPROCESSED_TOPIC #  'preprocess'

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers
}



try:
    # Attempt to create a Kafka producer
    producer = Producer(producer_config)
    no_kafka_producer = True
    print("Kafka producer is available.")
except Exception as e:
    print("Failed to create Kafka producer. Error:", str(e))
    no_kafka_producer = True


def bytes_to_string(encoded_bytes):
    return encoded_bytes.decode()

# Function to publish messages
def publish_message(key, image):
    global no_kafka_producer
    # Convert the key to bytes
    key_bytes = key

    # Convert the image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    # Compress the image data using zlib
    image_bytes = zlib.compress(image_bytes.read())  
    print(f"image_bytes length after compression : {len(image_bytes)}")
    # Encode the image as base64 string
    image_data = b64encode(image_bytes).decode('utf-8')
  
    print(f"Message value : {image_data[:10]} ... {image_data[-10:]}")
    # Publish the message to the topic
    try:
        print(f"topic: {topic}")
        producer.produce(topic, key=key_bytes, value=image_data)
        producer.flush()
        no_kafka_producer = True
    except Exception as e:
        print("Failed to publish message to Kafka topic", str(e))
        no_kafka_producer = False
        


# Example usage
if __name__ == '__main__':
    # Read the image file as binary data
    image_path = './project/tests/bus.jpg'
    image = Image.open(image_path).convert("RGB")

    # Define the key
    key = uuid.uuid4()
    print(key)
    key =  str(key)

    # Publish the image to Kafka topic
    publish_message(key, image)