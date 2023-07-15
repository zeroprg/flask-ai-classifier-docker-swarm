from PIL import Image
import zlib
from io import BytesIO
import base64
import uuid

from rdkafka import RdKafka

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
topic = 'preprocessed'

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Create a Kafka producer
producer = RdKafka(RdKafka.Producer, producer_config)


def publish_message(key, image):
    # Convert the key to bytes
    key_bytes = key.encode()

    # Convert the image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    # Compress the image data using zlib
    compressed_bytes = zlib.compress(image_bytes.read())

    # Encode the compressed image as base64 string
    image_data = base64.b64encode(compressed_bytes).decode('utf-8')

    # Publish the message to the topic
    producer.produce(topic, key_bytes, image_data)


# Example usage
if __name__ == '__main__':
    # Read the image file as binary data
    image_path = './project/tests/bus.jpg'
    image = Image.open(image_path).convert("RGB")

    # Define the key
    key = str(uuid.uuid4())

    # Publish the image to Kafka topic
    publish_message(key, image)
