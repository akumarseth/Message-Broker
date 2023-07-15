import pika
import sys
import json
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

exchang_name = 'logs'
channel.exchange_declare(exchange=exchang_name, exchange_type='fanout')

def publish():
    msg_count = 0
    while True:
        msg_dict = {
            'msg': msg_count
        }
        msg = json.dumps(msg_dict)
        channel.basic_publish(exchange=exchang_name, routing_key='', body=msg)

        print("Send `{msg}` to exchange `{exchange}`".format(msg=msg, exchange=exchang_name))

        msg_count += 1
        time.sleep(1)


publish()
connection.close()
