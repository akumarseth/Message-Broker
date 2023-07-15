import pika
import sys
import time
import json
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

# message = ' '.join(sys.argv[1:]) or "Hello World!"


def publish():
    msg_count = 0
    while True:
        msg_dict = {
            'msg': msg_count
        }
        msg = json.dumps(msg_dict)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    
        print("Send `{msg}` to topic `{queue}`".format(msg=msg, queue=queue_name))
        
        msg_count += 1
        time.sleep(1)
        

publish()
connection.close()