import pika, sys
import os
import dotenv

dotenv.load_dotenv()

host_url=os.getenv('RABBITMQ_HOST')
port=os.getenv('RABBITMQ_PORT')
username=os.getenv('RABBITMQ_USERNAME')
password=os.getenv('RABBITMQ_PASSWORD')



def main():
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host=host_url, port=port, credentials=credentials)


    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue_name='python001'
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print("Received `{msg}` from topic `{queue}`".format(msg=body.decode(), queue=queue_name))

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
