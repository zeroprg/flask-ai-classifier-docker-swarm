from confluent_kafka import Consumer, Producer
from PIL import Image
import struct
from io import BytesIO
import numpy as np
import zlib
from base64 import b64encode, b64decode
from process_images import process_images
import binascii

# Kafka broker configuration
bootstrap_servers = '192.168.1.87:9092'
preprocessed_topic = 'preprocessed'


# Create consumer and producer configurations
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Create Kafka consumer and producer
consumer = Consumer(consumer_config)
producer = Producer(producer_config)

# Subscribe to the preprocessed topic
consumer.subscribe([preprocessed_topic])

# Function to convert bytes to long integer
def bytes_to_long(b):
    return struct.unpack('>Q', b)[0]

# Function to decode, decompress, and display the image
def decode_and_decompress(encoded_data):
    # Check if the input data is a valid base64 string
    try:
        decoded_data = b64decode(encoded_data)
    except binascii.Error:
        print("Error: Invalid base64 input")
        return None

    # Decompress the compressed image data
    decompressed_data = zlib.decompress(decoded_data)
    # Convert the decompressed data to a NumPy array
    image_array = np.frombuffer(decompressed_data, dtype=np.uint8)
    # Create a PIL image from the NumPy array
    image = Image.fromarray(image_array)
    return image

# Function to publish messages in batches
def publish_message_batch(keys, results):
    message_batch = []
    for key, result in zip(keys, results):
        # Access the filtered images and object counts from the result tuple
        filtered_images, object_counts = result

        # Publish each image and its corresponding label to the topic with the given key
        for image, label in filtered_images:
            # Compress the image data using zlib
            image = zlib.compress(image.tobytes())
            image = b64encode(image)
            # Add the message to the batch
            message_batch.append((label, image))

        # Print the object counts for the current result
        print("Object Counts:")
        for label, count in object_counts.items():
            print(f"Label: {label}, Count: {count}")

    # Publish the batch of messages to the topic
    producer.produce_batch(message_batch)
    
# Function to consume messages, process images, and publish the results
def read_and_delete_messages(batch_size=100):
    keys = []
    values = []
    while True:
        message = consumer.poll(timeout=1.0)

        if message is None:
            continue

        if message.error():
            # Handle error
            print(f"Error occurred: {message.error()}")
            break

        # Process the received message
        key_bytes = message.key()
        key = int.from_bytes(key_bytes, byteorder="big")
        value = message.value()
        print(f"Key: {key}")    

        print(f"Message value type: {type(value)}")
        print(f"Message value : {value[:10]} ... {value[-10:]}")
        # Accumulate keys and values
        keys.append(key)
        values.append(decode_and_decompress(value))

        # Commit the offset to mark the message as processed
        consumer.commit(message)

        # Process images in batches of batch_size
        if len(keys) >= batch_size:
            try:
                # Process the images
                processed_images = process_images(keys, values)

                # Publish the processed images to the postprocessed topic
                publish_message_batch(keys, processed_images)
            except Exception as e:
                print(f"Error processing images: {e}")

            # Clear the accumulated keys and values
            keys.clear()
            values.clear()

    # After processing all messages, process any remaining images
    if len(keys) > 0:
        try:
            # Process the remaining images
            processed_images = process_images(keys, values)

            # Publish the processed images to the postprocessed topic
            publish_message_batch(keys, processed_images)
        except Exception as e:
            print(f"Error processing images: {e}")

    # Close the consumer and producer after processing all messages
    consumer.close()
    producer.flush()
    producer.close()

if (__name__ == "__main__"):
        read_and_delete_messages()