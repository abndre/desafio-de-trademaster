import pika
import json
import os
import uuid
from datetime import datetime

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_username = 'guest'
rabbitmq_password = 'guest'
rabbitmq_queue = 'aluguel_venda'

# Create the /data/events directory if it doesn't exist
os.makedirs('./data/events', exist_ok=True)

# Callback function for consuming messages
def callback(ch, method, properties, body):
    # Decode the message from bytes to a string
    message = body.decode('utf-8').replace("'", '"')

    # Parse the message as JSON
    event = json.loads(message)
    
    # Generate a unique filename using UUID and current datetime
    filename = str(uuid.uuid4()) + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.json'
    
    # Add the "data_ref" key to the event JSON
    event['data_ref'] = datetime.now().isoformat()
    
    # Save the event as a JSON file
    file_path = f'./data/events/{filename}'
    with open(file_path, 'w') as file:
        json.dump(event, file)
    
    print(f'Saved event: {event} to {filename}')

# Connect to RabbitMQ and consume messages
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password))
)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)

print('Consumer started. Waiting for messages...')

# Start consuming messages
channel.start_consuming()
