using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MQTT_Subscriber
{
    public static class cLog
    {
        private static readonly string LogFilePath = "Log.txt"; // Path to your log file

        // Method to write a message to the log file
        public static void WriteLog(string message)
        {
            try
            {
                // Create or append to the log file
                using (StreamWriter writer = File.AppendText(LogFilePath))
                {
                    writer.WriteLine($"{DateTime.Now} - {message}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error writing to log file: {ex.Message}");
            }
        }
    }
}
