import pika
import time
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

queue_name='task_queue'
channel.queue_declare(queue=queue_name, durable=True)
print('Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print("Received `{msg}` from topic `{queue}`".format(msg=body.decode(), queue=queue_name))
    # time.sleep(body.count(b'.'))
    # print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()