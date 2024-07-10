from xml.etree.ElementTree import tostring
import RPi.GPIO as GPIO  
import configparser,time

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve values from the configuration file
interval = int(config.get('Settings', 'interval')) 
device_name = config.get('Settings', 'device_name')
motion_sensor_pin = int(config.get('Settings', 'motion_sensor_gpio_pin'))   # Example GPIO pin
motion_sensor_type = config.get('Settings', 'motion_sensor_type')
# Set up GPIO mode and pin number
GPIO.setmode(GPIO.BCM) 

# Set up the PIR motion sensor pin as input
GPIO.setup(motion_sensor_pin, GPIO.IN)


def main():
    motion_detect()

def motion_detect():
    try: 
        return GPIO.input(motion_sensor_pin) 
 
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()  # Reset GPIO settings
 

if __name__ == "__main__":
    main()
