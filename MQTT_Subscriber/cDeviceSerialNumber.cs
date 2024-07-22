using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MQTT_Subscriber
{
    public static class cDeviceSerialNumber
    {
        public static string GetRaspberryPiSerial()
        {
            try
            {
                string[] lines = File.ReadAllLines("/proc/cpuinfo");

                foreach (string line in lines)
                {
                    if (line.StartsWith("Serial"))
                    {
                        // Extract the serial number
                        string serial = line.Split(':')[1].Trim();
                        return serial;
                    }
                }

                // If serial number is not found
                return null;
            }
            catch (FileNotFoundException)
            {
                // Handle the case where /proc/cpuinfo file is not found
                Console.WriteLine("/proc/cpuinfo file not found. Are you sure this is a Raspberry Pi?");
                return null;
            }
            catch (Exception ex)
            {
                // Handle other exceptions if necessary
                Console.WriteLine("An error occurred: " + ex.Message);
                return null;
            }
        }
    }
}
