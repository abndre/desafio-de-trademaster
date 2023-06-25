import pika
import json
import time

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_username = 'guest'
rabbitmq_password = 'guest'
rabbitmq_queue = 'aluguel_venda'

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)

# Define the event payload
event_payload = {
    "name": "joao",
    "message": "hello world"
}

# Publish events every 5 seconds
while True:
    # Convert the event payload to JSON
    event_json = json.dumps(event_payload)
    
    # Publish the event to the RabbitMQ queue
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=event_json)
    
    print(f'Published event: {event_json}')
    
    # Wait for 5 seconds before publishing the next event
    time.sleep(5)

# Close the connection to RabbitMQ
connection.close()
