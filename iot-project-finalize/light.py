import RPi.GPIO as GPIO  
import configparser, time

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve values from the configuration file
interval = int(config.get('Settings', 'interval')) 
device_name = config.get('Settings', 'device_name')
light_sensor_pin = int(config.get('Settings', 'light_sensor_gpio_pin'))   # Example GPIO pin
light_sensor_type = config.get('Settings', 'light_sensor_type')

# Set up GPIO mode and pin number
GPIO.setmode(GPIO.BCM)


# Set up the light sensor pin as input
GPIO.setup(light_sensor_pin, GPIO.IN)

def main():
     detect_light() 

def detect_light():
    try: 
        return GPIO.input(light_sensor_pin)
    
    except KeyboardInterrupt:
        print("Exiting program")
        GPIO.cleanup()

        
if __name__ == "__main__":
    main()