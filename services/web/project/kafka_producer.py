from confluent_kafka import Producer
import struct
from base64 import b64encode
from PIL import Image
from numpy import asarray
import zlib

# Kafka broker configuration
bootstrap_servers = '192.168.1.87:9092'
topic = 'preprocessed'

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

    # Compress the image data using zlib
    image = zlib.compress(image.tobytes())  
    image = b64encode(image)
  
    print(f"Message value : {image[:10]} ... {image[-10:]}")
    # Publish the message to the topic
    producer.produce(topic, key=key_bytes, value=image)
    producer.flush()

# Example usage
if __name__ == '__main__':
    # Read the image file as binary data
    image_path = './tests/woman_red.jpg'
    image = Image.open(image_path).convert("RGB")

    # Define the key
    key = 1234567890

    # Publish the image to Kafka topic
    publish_message(key, image)
