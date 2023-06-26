import pika
from util_consumer import check_content_message

# Função de callback para processar as mensagens
def callback(ch, method, properties, body):
    check_content_message(body)


rabbitmq_queue = 'aluguel_venda'


# Configuração da conexão RabbitMQ
rabbitmq_credentials = pika.PlainCredentials('guest', 'guest')
rabbitmq_parameters = pika.ConnectionParameters('localhost', 5672, '/', rabbitmq_credentials)
connection = pika.BlockingConnection(rabbitmq_parameters)
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)


print('Consumer started. Waiting for messages...')

# Start consuming messages
channel.start_consuming()