from confluent_kafka import Producer
import PIL
# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
topic = 'my-topic'

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Create Kafka producer
producer = Producer(producer_config)

# Function to publish messages
def publish_message(image_data):
    # Publish the message to the topic
    producer.produce(topic, value=image_data)
    producer.flush()

# Example usage
if __name__ == '__main__':
    image_path = './tests/background3.jpg'
    # Read and process the PIL Image
    image = PIL.Image.open(image_path) #.convert("RGB")

    # Convert the image to binary data
    image_data = image.tobytes()

    # Publish the binary data to Kafka topic
    publish_message(image_data)
