def get_raspberry_pi_serial():
    # Open the cpuinfo file
    try:
        with open('/proc/cpuinfo', 'r') as f:
            lines = f.readlines()

        # Search for the line containing the serial number
        for line in lines:
            if line.startswith('Serial'):
                # Extract the serial number
                serial = line.split(':')[1].strip()
                return serial

        # If serial number is not found
        return None
    except FileNotFoundError:
        # Handle the case where /proc/cpuinfo file is not found
        print("/proc/cpuinfo file not found. Are you sure this is a Raspberry Pi?")
        return None

# Example usage
serial_number = get_raspberry_pi_serial()
if serial_number:
    print("Raspberry Pi Serial Number:", serial_number)
else:
    print("Raspberry Pi Serial Number not found.")
