import json
import random
import time
import os
from paho.mqtt import client as mqtt_client
import dotenv

dotenv.load_dotenv()

broker=os.getenv('MQTT_HOST')
port=os.getenv('MQTT_PORT')
username=os.getenv('MQTT_USERNAME')
password=os.getenv('MQTT_PASSWORD')
 
topic = "python001"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
FLAG_CONNECTED = 0
 
 
def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )
 
 
def connect_mqtt():
    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
 
 
def publish(client):
    msg_count = 0
    while True:
        msg_dict = {
            'msg': msg_count
        }
        msg = json.dumps(msg_dict)
        result = client.publish(topic, msg, retain=True, qos=2)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send `{msg}` to topic `{topic}`".format(msg=msg, topic=topic))
        else:
            print("Failed to send message to topic {topic}".format(topic=topic))
        msg_count += 1
        time.sleep(1)
 
 
def run():
    client = connect_mqtt()
    client.loop_start()
    time.sleep(2)
    if FLAG_CONNECTED:
        publish(client)
    else:
        client.loop_stop()
 
 
if __name__ == '__main__':
    run()