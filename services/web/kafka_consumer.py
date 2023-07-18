from confluent_kafka import Consumer#, Producer
from PIL import Image
import struct
from io import BytesIO
import zlib
from base64 import b64decode, b64encode
from process_images import process_images, generate_hashcode
import binascii
from project import db
import time
import struct
import datetime

from project.config import  ProductionConfig as prod

# Kafka broker configuration
bootstrap_servers = prod.KAFKA_SERVER #'172.29.208.1:9092'
preprocessed_topic = prod.KAFKA_PREPROCESSED_TOPIC #  'preprocess'
#postprocessed_topic = prod.KAFKA_POSTPROCESSED_TOPIC #'postprocess'

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
#producer = Producer(producer_config)

# Subscribe to the preprocessed topic
consumer.subscribe([preprocessed_topic])


def long_to_bytes(n):
    return struct.pack('>Q', n)

# Function to save the decoded image
def save_image(image_bytes, image_path):
    with open(image_path, 'wb') as file:
        file.write(image_bytes)

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


    # Create a new PIL image from the decoded data
    image = Image.open(BytesIO(decompressed_data))

    return image



def publish_to_processed_topic(key, image, label):
    # Convert the image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    image_data = image_bytes.read()

    # Compress the image data using zlib
    compressed_data = zlib.compress(image_data)

    # Convert the compressed data to a base64-encoded string
    encoded_data = b64encode(compressed_data).decode('utf-8')

    # Prepare the message to send to Kafka
    #message = {
    #    'label': label,
    #    'timestamp': int(round(time.time() * 1000)),
    #    'data': encoded_data
    #}

    # Send the message to Kafka
    #producer.produce(postprocessed_topic, key=key, value=json.dumps(message).encode('utf-8'))
    #producer.flush()


# Function to publish messages in batches
def publish_message_batch(keys, results):
  
    for key, result in zip(keys, results):
        # Access the filtered images and object counts from the result tuple
        filtered_images, object_counts = result

        # Publish each image and its corresponding label to the topic with the given key
        for image, label in filtered_images:
            publish_to_processed_topic(key,image,label)

        # Print the object counts for the current result
        #print("Object Counts:")
        #for label, count in object_counts.items():
        #    print(f"Label: {label}, Count: {count}")



# Function to store messages in batches
def store_to_db_message_batch(keys, results):
    for key, result in zip(keys, results):
        # Access the filtered images and object counts from the result tuple
        filtered_images, object_counts = result
        # Store each image and its corresponding label to the database with the given key
        for image, label in filtered_images:
            # Generate a hashcode for the image
            hashcode = generate_hashcode(image)
            # Get the current date and time            
            now = datetime.datetime.now()
            # Format the datetime with the local timezone
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S %Z")  
            current_time =  int(time.time()*1000)
            #image_array = np.array(image)
            # Store the image and its metadata in the database
            db.insert_frame(hashcode, formatted_datetime, current_time, label, image, key)

        # Print the object counts for the current result
        #print("Object Counts:")
        #for label, count in object_counts.items():
        #    print(f"Label: {label}, Count: {count}")


    
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
   
        key = message.key().decode('utf-8')
        #print(message.timestamp())
        value = message.value()
        # Commit the offset to mark the message as processed
        consumer.commit(message)
        print(f"Key: {key}")
        #print(f"Message value type: {type(value)}")
        #print(f"Message value : {value[:10]} ... {value[-10:]}")
        # Accumulate keys and values
        keys.append(key)
        values.append(decode_and_decompress(value))

        #print(f"~~~ Here we are ~~~ ")
        # Process images in batches of batch_size
        if len(keys) >= batch_size or (len(keys) > 0 and consumer.poll(0) is None):
            try:
                tr = db.start_transaction()

                # Process the images
                processed_images = process_images(keys, values)

                # Publish the processed images to the postprocessed topic use it if necessary to proccess images in separate topic
                #publish_message_batch(keys, processed_images)

                # Store the processed images in the database
                store_to_db_message_batch(keys, processed_images)
                # use for big transactions 
                tr.commit()
            except Exception as e:
                print(f"Error processing images: {e}")
                # Roll back the transaction in case of an error
                tr.rollback()

            # Clear the accumulated keys and values
            keys.clear()
            values.clear()


    # Close the consumer and producer after processing all messages
    consumer.close()
    #producer.flush()
    #producer.close()

if (__name__ == "__main__"):
        read_and_delete_messages()