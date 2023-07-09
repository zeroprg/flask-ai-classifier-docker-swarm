from confluent_kafka import Consumer, KafkaError
from PIL import Image
from io import BytesIO
import datetime
from datetime import timedelta
import struct
from base64 import b64decode
import zlib
import binascii
import json
import time


from project.config import ProductionConfig as prod

# Kafka broker configuration
bootstrap_servers = prod.KAFKA_SERVER
topic = prod.KAFKA_POSTPROCESSED_TOPIC
group_id = 'my-consumer-group'

# Create Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

# Create Kafka consumer
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
consumer.subscribe([topic])

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
    # Consume messages from the Kafka topic
    while True:
        message = consumer.poll(timeout=1.0)
        if message is None:
            continue
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                # Reached the end of a partition
                break
            else:
                # Error occurred
                print("Error: {}".format(message.error().str()))
                continue

        _key = message.key().decode('utf-8')
        print(f"_key : {_key}")  
        # Commit the offset to mark the message as processed
        consumer.commit(message)
        
        value = json.loads(message.value().decode('utf-8'))     
        print(f"label : {value['label']}")       
        if 'timestamp' not in value:
            continue
        timestamp = int(value['timestamp'])            
        # Retrieve the image data from the message
        image_data = value['data']

        # Create a PIL Image from the image data
        image = decode_and_decompress_image(image_data)

        # Yield the image to the caller
        yield image


def yield_saved_images(start_time_ms, end_time_ms, key, label):
     # Get images from the Kafka topic within the specified time range and conditions
    image_generator = get_images_from_topic(start_time_ms, end_time_ms, key, label)
        # Variables to track inactivity timeout
    #start_time = time.time()
    #timeout = 10  # Timeout in seconds
    # Iterate through the images
    for i,image in enumerate(image_generator):
        # Do something with each image (e.g., display, save, etc.)
        image.save(f"TestPIL{i}.jpg")
        print(f"Image {image} {i} here ")
                # Check for inactivity timeout
        # Check for inactivity timeout
        #if time.time() - start_time > timeout:
        #    print("Inactivity timeout reached. Exiting the loop.")
        #    break



# Example usage
if __name__ == '__main__':
    # Define the key, time range in minutes, and label
    key = 'c127426f-e208-4fed-bfa6-d3aa47f55ef4'
    label = 'person'
    # Calculate start and end time based on minutes back from current time
    start_minutes_back = 360  # Replace with the desired number of minutes
    end_minutes_back = 0  # Replace with the desired number of minutes

    current_time = datetime.datetime.now()
    start_time = current_time - timedelta(minutes=start_minutes_back)
    end_time = current_time - timedelta(minutes=end_minutes_back)

    # Convert start_time and end_time to milliseconds
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)


    # print(image_generator)
    # Process the retrieved images as needed
    yield_saved_images(start_time_ms, end_time_ms, key, label)

