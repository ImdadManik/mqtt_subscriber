from mqtt_connect import client, connect_to_broker, disconnect_from_broker
import door, light, motion, temp # type: ignore
import time, sr, json 
import RPi.GPIO as GPIO  
import configparser

#import packages for motion sensors
# Create a ConfigParser object
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
ldr_value = None
ldr_alert_freq = None

door_value = None
pir_value = None 

motion_detected = False
door_detected = False
_retain = False
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
 

# Message receiving callback
def on_message(client, userdata, msg): 
    global payload_data
    global temp_value
    global temp_alert_freq
    global ldr_value
    global ldr_alert_freq
    global all_sensor_status
    global door_value
    global pir_value
    
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
    GPIO.add_event_detect(door_sensor_pin, GPIO.BOTH, callback=door_sensor_callback)
    GPIO.add_event_detect(motion_sensor_pin, GPIO.RISING, callback=motion_detected_callback)

    start_time_temp = time.time()
    start_time_ldr = time.time()

    # Publish and subscribe loop
    try:  
        while (True):
            if motion_detected: 
                push_PIR_reading  # Publish motion detection event

            client.subscribe(sub_setting_Topic, qos=1)
            client.on_message = on_message

            # Publish message
            if payload_data is not None:
                if all_sensor_status: 

                    if temp_value is True and temp_alert_freq:
                        if time.time() - start_time_temp >= temp_alert_freq:
                            client.publish(pub_Temp_Topics, str(temp.getTemperature()) +',' + str(temp.getHumidity())  , retain=_retain)
                            print('----temp')
                            start_time_temp = time.time()
                    
                    if ldr_value is True and ldr_alert_freq:
                        if time.time() - start_time_ldr >= ldr_alert_freq:
                            client.publish(pub_Ldr_Topics, light.detect_light(), retain=_retain)
                            print('----ldr')
                            start_time_ldr = time.time()

            time.sleep(interval)
    except KeyboardInterrupt:
        # Disconnect from the broker
        disconnect_from_broker()

