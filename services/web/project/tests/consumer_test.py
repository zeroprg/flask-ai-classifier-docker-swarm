import json
from confluent_kafka import Consumer

# Create Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

# Create Kafka consumer
consumer = Consumer(consumer_config)

# Subscribe to the topic
consumer.subscribe(['your_topic_name'])

# Consume messages
while True:
    message = consumer.poll(1.0)
    
    if message is None:
        continue
    
    if message.error():
        print(f"Consumer error: {message.error()}")
        break
    
    # Deserialize the message from JSON
    json_data = message.value().decode()
    obj_data = json.loads(json_data)
    
    # Create an instance of your class from the deserialized data
    my_object = MyClass(obj_data['name'])
    
    # Process the object as needed
    print(f"Received object: {my_object.name}")
    
    # Commit the offset to mark the message as processed
    consumer.commit(message)
