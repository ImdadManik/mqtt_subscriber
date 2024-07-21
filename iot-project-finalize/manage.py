import door, light, motion, temp # type: ignore
import configparser, json, sr # type: ignore


# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')
var_temp = True
var_hum = True
var_door = True
var_ldr = True
var_pir = True
# Retrieve values from the configuration file
device = config.get('Settings', 'device_name')
data = {}

def generatePayload(payload):
    global var_temp
    global var_door
    global var_ldr
    global var_pir
    if payload is not None:
        datajson = json.loads(payload)
        print("manage.py : "+ payload)
        var_temp = datajson['Temp']
        var_door = datajson['Door']
        var_ldr =  datajson['LDR']
        var_pir =  datajson['PIR']

    _temperature_c = temp.getTemperature() if var_temp == True else None
    _humidity = temp.getHumidity() if var_temp == True else None
    _door = door.door_detections() if var_door == True else None
    _ldr = light.detect_light() if var_ldr == True else None
    _pir = motion.motion_detect() if var_pir == True else None
    _sr = sr.get_raspberry_pi_serial()

    data = {
        "CLIENTID": _sr,
        "DOOR": str(_door),
        "LDR":  str(_ldr),
        "PIR":str(_pir),
        "HUMIDITY": str(_humidity),
        "TEMPERATURE": str(_temperature_c)
    }
    json_string  = json.dumps(data)
    return json_string
