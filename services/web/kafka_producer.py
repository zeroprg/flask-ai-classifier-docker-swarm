from confluent_kafka import Producer
import struct
from base64 import b64encode
from PIL import Image
import zlib
from io import BytesIO 

from project.config import  ProductionConfig as prod

# Kafka broker configuration
bootstrap_servers = prod.KAFKA_SERVER #'172.29.208.1:9092'
topic = 'preprocessed'# prod.KAFKA_PREPROCESSED_TOPIC #  'preprocess'

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Create Kafka producer
producer = Producer(producer_config)

# Function to convert long integer to bytes
def long_to_bytes(n):
    return struct.pack('>Q', n)

def bytes_to_string(encoded_bytes):
    return encoded_bytes.decode()

# Function to publish messages
def publish_message(key, image):
    # Convert the key to bytes
    key_bytes = long_to_bytes(key)

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
    print(f"topic: {topic}")
    producer.produce(topic, key=key_bytes, value=image_data)
    producer.flush()

# Example usage
if __name__ == '__main__':
    # Read the image file as binary data
    image_path = './project/tests/bus.jpg'
    image = Image.open(image_path).convert("RGB")

    # Define the key
    key = 1234567890

    # Publish the image to Kafka topic
    publish_message(key, image)
