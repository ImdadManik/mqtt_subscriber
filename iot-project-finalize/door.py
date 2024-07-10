from operator import truediv
import RPi.GPIO as GPIO
import configparser, time

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve values from the configuration file
interval = int(config.get('Settings', 'interval'))
device_name = config.get('Settings', 'device_name')
door_sensor_type = config.get('Settings','door_sensor_type')
door_sensor_pin = int(config.get('Settings', 'door_sensor_gpio_pin')) # Example GPIO pin

# Set up GPIO mode and pin number
GPIO.setmode(GPIO.BCM)

# Set up the door sensor pin as input
GPIO.setup(door_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main(): 
    door_detections()
    

def door_detections():
    try:
        return GPIO.input(door_sensor_pin)                

    except KeyboardInterrupt:
        print("Exiting program")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
