import json
from platform import node
from mqtt_connect import client, connect_to_broker, disconnect_from_broker
import time 

subTopic = "device/00000000daeca42f"

payload_data = None

#publishers topics
pub_Ldr_Topics='sensor/Ldr/'
pub_Temp_Topics='sensor/Temp/'
pub_Pir_Topics='sensor/Pir/'
pub_Door_Topics='sensor/Door/'
#end publishers topics

#global variables
all_sensor_status = None 
temp_value = None
temp_alert_freq = None 
ldr_value = None
ldr_alert_freq = None

door_value = None
pir_value = None 
#end global variables

def on_message(client, userdata, msg):
    global payload_data
    global temp_value
    global temp_alert_freq
    global ldr_value
    global ldr_alert_freq
    global all_sensor_status

    global door_value
    global pir_value  

    if msg.topic == subTopic:
        payload_data = msg.payload.decode()
        payload_dict = json.loads(payload_data)
        temp_value = payload_dict.get('Temp')
        temp_alert_freq = payload_dict.get('TempAlertFreq')
        ldr_value = payload_dict.get('LDR')
        ldr_alert_freq = payload_dict.get('LDRAlertFreq')
        all_sensor_status = payload_dict.get('Status')
        door_value = payload_dict.get('Door')
        pir_value = payload_dict.get('PIR')

if __name__ == "__main__":
    connect_to_broker()
    start_time_temp = time.time()
    start_time_ldr = time.time()

    try:
        while (True):
            client.subscribe(subTopic, qos=1)
            client.on_message = on_message

            if payload_data is not None:
                if all_sensor_status:
                    print('')
                    print('Status')
                    print(all_sensor_status)
                    print('')
                    if temp_value is True and temp_alert_freq:
                        print('temp')
                        print(temp_value)
                        print(temp_alert_freq)
                        if time.time() - start_time_temp >= temp_alert_freq:
                            start_time_temp = time.time()
                    
                    if ldr_value is True and ldr_alert_freq:
                        print('')
                        print('ldr')
                        print(ldr_value)
                        print(ldr_alert_freq)
                        if time.time() - start_time_ldr >= ldr_alert_freq:
                            start_time_ldr = time.time()

            time.sleep(5)

    except KeyboardInterrupt:
        # Disconnect from the broker
        disconnect_from_broker()

