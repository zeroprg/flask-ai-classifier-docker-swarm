from confluent_kafka import KafkaConsumer
from PIL import Image
from io import BytesIO
import datetime
from datetime import timedelta
import struct 
from base64 import b64decode
import zlib
import binascii

from project.config import  ProductionConfig as prod

# Kafka broker configuration
bootstrap_servers = prod.KAFKA_SERVER #'172.29.208.1:9092'
topic = prod.KAFKA_POSTPROCESSED_TOPIC #'postprocess'

group_id = 'my-consumer-group'

# Create Kafka consumer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=bootstrap_servers,
                         group_id=group_id,
                         value_deserializer=lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

# Function to convert bytes to long integer
def bytes_to_long(b):
    return struct.unpack('>Q', b)[0]

# Function to decode, decompress, and display the image
def decode_and_decompress_image(encoded_data):
    # Check if the input data is a valid base64 string
    try:
        decoded_data = b64decode(encoded_data)
    except binascii.Error:
        print("Error: Invalid base64 input")
        return None

    # Decompress the compressed image data
    decompressed_data = zlib.decompress(decoded_data)


    # Create a new PIL image from the decoded data
    image = Image.open(BytesIO(decompressed_data))

    return image

def get_images_from_topic(start_time_ms, end_time_ms, key, label):
    # List to store the retrieved images
    images = []

    # Consume messages from the Kafka topic
    for message in consumer:
        value = message.value
        # use it if there is problem with decoding timestamp = bytes_to_long(value['timestamp'])
        timestamp = value['timestamp']
        # Check if the key, timestamp, and label match
        if value['key'] == key and start_time_ms <= timestamp <= end_time_ms and label in value['label']:
            # Retrieve the image data from the message
            image_data = value['data']

            # Create a PIL Image from the image data
            image = decode_and_decompress_image(image_data)

            # Append the image to the list
            images.append(image)

        # Break the loop if the end_time is reached
        if value['timestamp'] > end_time_ms:
            break

    return images

# Example usage
if __name__ == '__main__':
    # Define the key, time range in minutes, and label
    key = 'your_key_here'
    label ="person"
    # Calculate start and end time based on minutes back from current time
    start_minutes_back = 60  # Replace with the desired number of minutes
    end_minutes_back = 0  # Replace with the desired number of minutes

    current_time = datetime.datetime.now()
    start_time = current_time - timedelta(minutes=start_minutes_back)
    end_time = current_time - timedelta(minutes=end_minutes_back)

    # Convert start_time and end_time to milliseconds
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    # Get images from the Kafka topic within the specified time range and conditions
    images = get_images_from_topic(start_time_ms, end_time_ms, key, label)

    # Process the retrieved images as needed
    for image in images:
        # Do something with each image (e.g., display, save, etc.)
        image.show()
