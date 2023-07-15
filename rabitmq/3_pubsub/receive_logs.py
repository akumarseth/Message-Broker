import pika
import os
import dotenv

dotenv.load_dotenv()

host_url=os.getenv('RABBITMQ_HOST')
port=os.getenv('RABBITMQ_PORT')
username=os.getenv('RABBITMQ_USERNAME')
password=os.getenv('RABBITMQ_PASSWORD')

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=host_url, port=port, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

exchang_name = 'logs'
channel.exchange_declare(exchange=exchang_name, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=exchang_name, queue=queue_name)

print('Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print("Received `{msg}` from exchange `{exhange}` with queue `{queue}`".format(msg=body.decode(), exhange=exchang_name, queue=queue_name))    

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()