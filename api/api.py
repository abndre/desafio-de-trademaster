from flask import Flask, request
import pika

app = Flask(__name__)

# RabbitMQ connection parameters
rabbitmq_credentials = pika.PlainCredentials('guest', 'guest')
rabbitmq_parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', rabbitmq_credentials)

@app.route('/send_event', methods=['POST'])
def send_event():
    try:
        # Establish a connection to RabbitMQ
        connection = pika.BlockingConnection(rabbitmq_parameters)
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='aluguel_venda')

        # Get the event data from the request
        event_data = request.get_json()

        # Convert the event data to a string
        message = str(event_data)

        # Publish the message to the queue
        channel.basic_publish(exchange='', routing_key='aluguel_venda', body=message)

        # Close the connection
        connection.close()

        return 'Event sent successfully'
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)