from mqtt_connect import client, connect_to_broker, disconnect_from_broker
import door, light, motion, temp
import time, sr, json
import RPi.GPIO as GPIO
import configparser

#Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve values from the configuration file
interval = int(config.get('Settings', 'interval'))
motion_sensor_pin = int(config.get('Settings', 'motion_sensor_gpio_pin'))   # Example GPIO pin
door_sensor_pin = int(config.get('Settings', 'door_sensor_gpio_pin')) # Example GPIO pin

# Set up GPIO mode and pin number
GPIO.setmode(GPIO.BCM)

# Set up the PIR motion sensor pin as input with pull-down resistor
GPIO.setup(motion_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set up the door sensor pin as input
GPIO.setup(door_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback function to handle motion detection event
def motion_detected_callback(channel):
    global motion_detected
    if pir_value and all_sensor_status:
        push_PIR_reading()  # Motion detected, send sensor reading
        motion_detected = True

# Callback function to handle door sensor event
def door_sensor_callback(channel):
    global door_detected
    if door_value and all_sensor_status:
        push_Door_reading()
        door_detected = True

def push_PIR_reading():
    print('----motion')
    client.publish(pub_Pir_Topics, motion.motion_detect(), retain=_retain)


def push_Door_reading():
    print('-----door')
    client.publish(pub_Door_Topics, door.door_detections(), retain=_retain)

# Global variable to store motion and door detection status
payload_data = None
all_sensor_status = None
temp_value = None
temp_alert_freq = None
min_temp_alert = None
ldr_value = None
ldr_alert_freq = None

door_value = None
pir_value = None

motion_detected = False
door_detected = False
_retain = True

#for filter the device from heartbeat topics
account_id = None
device_id = None
# end variable declarations

# subscriber topics to get the device settings from retain message
sub_setting_Topic = "device/" + sr.get_raspberry_pi_serial()
# end subscriber topics

#publishers topics
pub_Ldr_Topics='sensor/Ldr/'+ sr.get_raspberry_pi_serial()
pub_Temp_Topics='sensor/Temp/'+ sr.get_raspberry_pi_serial()
pub_Pir_Topics='sensor/Pir/'+ sr.get_raspberry_pi_serial()
pub_Door_Topics='sensor/Door/'+ sr.get_raspberry_pi_serial()
#end publishers topics

#heartbeat topic
pub_connect_topics = 'device/connected/' + sr.get_raspberry_pi_serial()

# Global variables to track last retain message and state
last_retain_message = None

def diconnectPublishMsg():
    global account_id, device_id
    data = {
        "AccountId": account_id,
        "Id": device_id,
        "IsConnected":  'disconnected'
    }
    json_string  = json.dumps(data)
    #print(f"Disconnected Msgs : {json_string}")
    return json_string

def connectedPublishMsg():
    global account_id, device_id
    data = {
        "AccountId": account_id,
        "Id": device_id,
        "IsConnected":  'connected'
    }
    json_string  = json.dumps(data)
    #print(f"Connected Msgs : {json_string}")
    client.publish(pub_connect_topics, json_string, retain=_retain)

# Message receiving callback
def on_message(client, userdata, msg):
    global payload_data
    global temp_value
    global temp_alert_freq
    global min_temp_alert
    global ldr_value
    global ldr_alert_freq
    global all_sensor_status
    global door_value
    global pir_value
    global account_id
    global device_id
    global last_retain_message

    payload_dict=None


    if msg.topic == sub_setting_Topic and msg.payload is not None:
        last_retain_message = msg.payload  # Update last_retain_message
        payload_data = msg.payload.decode()
        payload_list = json.loads(payload_data)
        # Check if payload_list is a list (which indicates it's an array of objects)
        if isinstance(payload_list, list):
            if len(payload_list) > 0:  
                payload_dict = payload_list[0]  # Take the first object from the array
            else:  
                print("Error: Empty JSON array received.")
                return
        else:
            payload_dict = payload_list  # It's a single object
            
        if msg.payload != last_retain_message:
            temp_value = bool(payload_dict.get('Temp', temp_value))
            temp_alert_freq = payload_dict.get('TempAlertFreq', temp_alert_freq)
            min_temp_alert =payload_dict.get('MinTempAlert', min_temp_alert)
            ldr_value = bool(payload_dict.get('LDR', ldr_value))
            ldr_alert_freq = payload_dict.get('LDRAlertFreq', ldr_alert_freq)
            all_sensor_status = bool(payload_dict.get('Status', all_sensor_status))
            door_value = bool(payload_dict.get('Door', door_value))
            pir_value = bool(payload_dict.get('PIR', pir_value))
            account_id = payload_dict.get('AccountId', account_id)
            device_id =  payload_dict.get('Id', device_id)
        else:
            temp_value = bool(payload_dict.get('Temp', temp_value))
            temp_alert_freq = payload_dict.get('TempAlertFreq', temp_alert_freq)
            min_temp_alert =payload_dict.get('MinTempAlert', min_temp_alert)
            ldr_value = bool(payload_dict.get('LDR', ldr_value))
            ldr_alert_freq = payload_dict.get('LDRAlertFreq', ldr_alert_freq)
            all_sensor_status = bool(payload_dict.get('Status', all_sensor_status))
            door_value = bool(payload_dict.get('Door', door_value))
            pir_value = bool(payload_dict.get('PIR', pir_value))
            account_id = payload_dict.get('AccountId', account_id)
            device_id =  payload_dict.get('Id', device_id) 
        connectedPublishMsg()
         
    # if msg.topic == sub_setting_Topic and msg.payload is not None:   
    #     if msg.payload != last_retain_message:            
    #         last_retain_message = msg.payload  # Update last_retain_message
    #         payload_data = msg.payload.decode()
    #         try:
    #             payload_list = json.loads(payload_data)
    #             # Check if payload_list is a list (which indicates it's an array of objects)
    #             if isinstance(payload_list, list):
    #                 if len(payload_list) > 0:  
    #                     payload_dict = payload_list[0]  # Take the first object from the array
    #                 else:  
    #                     print("Error: Empty JSON array received.")
    #                     return
    #             else:
    #                 payload_dict = payload_list  # It's a single object 
 
    #             temp_value = bool(payload_dict.get('Temp', temp_value))
    #             temp_alert_freq = payload_dict.get('TempAlertFreq', temp_alert_freq)
    #             min_temp_alert =payload_dict.get('MinTempAlert', min_temp_alert)
    #             ldr_value = bool(payload_dict.get('LDR', ldr_value))
    #             ldr_alert_freq = payload_dict.get('LDRAlertFreq', ldr_alert_freq)
    #             all_sensor_status = bool(payload_dict.get('Status', all_sensor_status))
    #             door_value = bool(payload_dict.get('Door', door_value))
    #             pir_value = bool(payload_dict.get('PIR', pir_value))
    #             account_id = payload_dict.get('AccountId', account_id)
    #             device_id =  payload_dict.get('Id', device_id)
    #             #print("after if payload_dict ")
    #             #print("")
    #             #print("---------------------------------------------------------------------------------------------------------")
    #             #print(f"temp value : {temp_value} | TempAlertFreq: {temp_alert_freq} | ldr value : {ldr_value} | LDRAlertFreq : {ldr_alert_freq} | Status: {all_sensor_status} | Door: {door_value} | PIR: {pir_value} | AccountId: {account_id} | DeviceId: {device_id}")
    #             #print("---------------------------------------------------------------------------------------------------------")
    #         except json.JSONDecodeError as e:
    #             print(f"Error decoding JSON: {e}")
    #         except Exception as e:
    #             print(f"Error processing message: {e}")
    #     else:
    #         payload_data = msg.payload.decode()
    #         temp_value = bool(payload_data.get('Temp', temp_value))
    #         temp_alert_freq = payload_data.get('TempAlertFreq', temp_alert_freq)
    #         min_temp_alert =payload_data.get('MinTempAlert', min_temp_alert)
    #         ldr_value = bool(payload_data.get('LDR', ldr_value))
    #         ldr_alert_freq = payload_data.get('LDRAlertFreq', ldr_alert_freq)
    #         all_sensor_status = bool(payload_data.get('Status', all_sensor_status))
    #         door_value = bool(payload_data.get('Door', door_value))
    #         pir_value = bool(payload_data.get('PIR', pir_value))
    #         account_id = payload_data.get('AccountId', account_id)
    #         device_id =  payload_data.get('Id', device_id)

       
if __name__ == "__main__":
    try: 
        connect_to_broker()
        client.subscribe(sub_setting_Topic)
        client.on_message = on_message
        connectedPublishMsg()
        client.loop_start()

        GPIO.add_event_detect(door_sensor_pin, GPIO.BOTH, callback=door_sensor_callback)
        GPIO.add_event_detect(motion_sensor_pin, GPIO.RISING, callback=motion_detected_callback)
   
        start_time_temp = time.time()
        start_time_ldr = time.time()

        while True:
            if client.is_connected():
                if motion_detected:
                    push_PIR_reading  #Publish motion detection event 

                if payload_data is not None:
                    if all_sensor_status: 
                        #if temp.getTemperature() is not None:
                        # if temp_value is True and temp_alert_freq and (temp.getTemperature() > min_temp_alert):
                        #     if time.time() - start_time_temp >= temp_alert_freq:
                        #         client.publish(pub_Temp_Topics, str(temp.getTemperature()) +',' + str(temp.getHumidity())  , retain=_retain)
                        #         print('----temp')
                        #         start_time_temp = time.time()

                        if ldr_value is True and ldr_alert_freq:
                                    if time.time() - start_time_ldr >= ldr_alert_freq:
                                        client.publish(pub_Ldr_Topics, light.detect_light(), retain=_retain)
                                        print('----ldr')
                                        start_time_ldr = time.time()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Disconnecting...")
        disconnect_from_broker(diconnectPublishMsg())
    except Exception as e:
        print("An error occurred:", e)
        disconnect_from_broker(diconnectPublishMsg())
    finally:
        disconnect_from_broker(diconnectPublishMsg())