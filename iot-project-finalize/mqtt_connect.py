
import paho.mqtt.client as mqtt
import EasyAES, sr  # type: ignore

aes = EasyAES.EasyAES('098pub+1key+0pri', 256, 'ABCXYZ123098')

# MQTT broker settings
broker_address = "pms-db003.fandaqah.com"  # Replace with your EMQX broker address
port = 1883  # Replace with your broker port 
client_id = sr.get_raspberry_pi_serial()
username = client_id
password = aes.encrypt(username)

pub_connect_topics = 'device/connected/' + username
retain = True

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)

def on_connect(client, userdata, flags, rc): 
    if rc == 0:
        client.publish(pub_connect_topics, 'connected', retain=retain)       
        print("Connected to MQTT Broker!") 

def connect_to_broker():  
    if not client.is_connected():
        client.username_pw_set(username, password)   
        client.on_connect = on_connect
        client.connect(broker_address, port)
        client.loop_start()
    
def disconnect_from_broker(): 
    if client.is_connected():
        client.publish(pub_connect_topics, 'disconnected', retain=retain)
        client.loop_stop() 
        client.disconnect()
        print("Disconnected from MQTT Broker") 
 
