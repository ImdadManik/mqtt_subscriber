import time
import board
import adafruit_dht 
dhtDevice = adafruit_dht.DHT11(board.D19) 

def main():
    getTemperature() 


def getTemperature():
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        if temperature_c is not None:
            return temperature_c
        else:
            print('Failed to retrieve data from DHT22 sensor')

    except RuntimeError as error:     
        print("Exiting program")

def getHumidity():
    try: 
        humidity = dhtDevice.humidity
        if humidity is not None:
            return humidity
        else:
            print('Failed to retrieve data from DHT22 sensor')

    except RuntimeError as error:     
        print("Exiting program")
    

if __name__ == "__main__":
    main()