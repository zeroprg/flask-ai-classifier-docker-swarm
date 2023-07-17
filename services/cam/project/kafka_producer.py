from base64 import b64encode
from PIL import Image
import zlib
from io import BytesIO
import uuid
from pykafka import KafkaClient

from project.config import ProductionConfig as prod

# Kafka broker configuration
bootstrap_servers = prod.KAFKA_SERVER  # '172.29.208.1:9092'
topic = prod.KAFKA_PREPROCESSED_TOPIC  # 'preprocess'

#bootstrap_servers = '192.168.0.197:9092'
#topic = 'preprocessed'
#partition_number = 0 # Random

no_kafka_producer =True
# Create Kafka client
kafka_client = KafkaClient(hosts=bootstrap_servers)

# Get the Kafka topic
kafka_topic = kafka_client.topics[topic]

# Create a producer with delivery reports enabled
producer = kafka_topic.get_sync_producer() # .get_producer(delivery_reports=True)

def bytes_to_string(encoded_bytes):
    return encoded_bytes.decode()

# Function to handle message delivery report when using delivery_reports=True in asynchronous producer
def check_delivery_reports():
    for message in producer.get_delivery_reports():
        if message is not None:
            if message[0] is not None:
                print(f"Failed to deliver message: {message[0]}")
            else:
                print(f"Message delivered to {message[1].topic} [{message[1].partition}]")

# Function to publish messages
def publish_message(key, image):
    # Convert the key to bytes
    key_bytes = key.encode()

    # Convert the image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    # Compress the image data using zlib
    compressed_image_bytes = zlib.compress(image_bytes.read())
    print(f"image_bytes length after compression : {len(compressed_image_bytes)}")

    # Encode the image as base64 string
    image_data = b64encode(compressed_image_bytes).decode('utf-8')
    #print(f"Message value : {image_data[:10]} ... {image_data[-10:]}")

    # Publish the message to the topic
    try:
        producer.produce( image_data.encode('utf-8'), partition_key=key_bytes)
        print(f"Message published successfully. for cam id= {key}")
        no_kafka_producer = False
        #check_delivery_reports()
    except Exception as e:
        print("Failed to publish message to Kafka topic:", str(e))
        no_kafka_producer = True

# Example usage
if __name__ == '__main__':
    # Read the image file as binary data
    image_path = '../tests/bus.jpg'
    image = Image.open(image_path).convert("RGB")

    # Define the key
    key = str(uuid.uuid4())
    print(key)

    # Publish the image to Kafka topic
    for i in range(10):
        publish_message(key, image)
