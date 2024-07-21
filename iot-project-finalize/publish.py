# python 3.8
import time
import manage , sr
from paho.mqtt import client as mqtt_client
import EasyAES


aes = EasyAES.EasyAES('098pub+1key+0pri', 256, 'ABCXYZ123098')

broker = '192.168.1.24' #'e47dee11.emqx.cloud'
port = 1883
topic = "sensor/data"
# generate client ID with pub prefix randomly
client_id = sr.get_raspberry_pi_serial()
username = client_id
password = aes.encrypt(client_id)


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        time.sleep(3)
        msg = str(manage.generatePayload())
        print(msg)
        result = client.publish(topic, msg)
        # result: [0, 1] # type: ignore
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)



if __name__ == '__main__':
    run()
