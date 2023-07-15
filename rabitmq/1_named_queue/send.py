import pika
import json
import time
import os
import dotenv

print(os.getcwd())

dotenv.load_dotenv()

host_url=os.getenv('RABBITMQ_HOST')
port=os.getenv('RABBITMQ_PORT')
username=os.getenv('RABBITMQ_USERNAME')
password=os.getenv('RABBITMQ_PASSWORD')

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=host_url, port=port, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

queue_name='python001'

channel.queue_declare(queue=queue_name)

def publish():
    msg_count = 0
    while True:
        msg_dict = {
            'msg': msg_count
        }
        msg = json.dumps(msg_dict)
        channel.basic_publish(exchange='', routing_key=queue_name, body=msg)
        print("Send `{msg}` to topic `{queue}`".format(msg=msg, queue=queue_name))
        
        msg_count += 1
        time.sleep(1)
    
       
publish()
connection.close()
