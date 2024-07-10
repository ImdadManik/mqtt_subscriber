using MySql.Data.MySqlClient;
using System;
using Newtonsoft;
using Newtonsoft.Json;

namespace MQTT_Subscriber
{
    public static class cMyDAL
    {
        static string connectionString = "server=192.168.1.24;port=3307;user=IOTPortal;database=IOTPortal;password=Fandaqah@2020";
        public static void addSensorDatas(string topics, emqx_msgs emqx_Msgs)
        {
            // Create a MySqlConnection object
            using (MySqlConnection connection = new MySqlConnection(connectionString))
            {
                try
                {
                    // Open the connection
                    connection.Open();
                    string qry = "INSERT INTO IOTPortal.sensors_msgs(client_id, msg_data, topics, msg_type) VALUES(@client_id, @msg_data, @topics, @msg_type);";
                    //string query = "INSERT INTO `sensordata`(`topics`, `payloads`) VALUES (@topics, @payloads)";

                    // Create a MySqlCommand object with the SQL statement and connection
                    using (MySqlCommand command = new MySqlCommand(qry, connection))
                    {
                        // Add parameters to the command
                        command.Parameters.AddWithValue("@client_id", emqx_Msgs.CLIENTID);
                        command.Parameters.AddWithValue("@msg_data", emqx_Msgs.MSGDATA);
                        command.Parameters.AddWithValue("@msg_type", emqx_Msgs.MSGTYPE.ToUpper());
                        command.Parameters.AddWithValue("@topics", topics);
                        
                        // Execute the command
                        int rowsAffected = command.ExecuteNonQuery();
                        cLog.WriteLog(rowsAffected.ToString());
                        cLog.WriteLog(rowsAffected > 0 ? "Data inserted successfully." : "Failed to insert data."); 
                    }
                }
                catch (Exception ex)
                {
                    cLog.WriteLog(ex.Message);
                }
            }
        }

        public static string GetDeviceSettings(string username)
        {
            using (MySqlConnection connection = new MySqlConnection(connectionString))
            {
                try
                {
                    // Open the connection
                    connection.Open();

                    // Create a MySqlCommand object with the SQL statement and connection
                    using (MySqlCommand command = new MySqlCommand("SELECT JSON_OBJECT(id, id, name, Name, msg_data, msg_data, topics, topics, msg_type, msg_type) AS json_payload FROM IOTPortal.sensors_msgs WHERE Name = @name;", connection))
                    {
                        // Add parameter to the command
                        command.Parameters.AddWithValue("@name", username);

                        // Execute the command
                        using (MySqlDataReader reader = command.ExecuteReader())
                        {
                            // Check if any rows were returned
                            if (reader.HasRows)
                            {
                                // Read the rows and create a list of JSON strings
                                List<string> jsonList = new List<string>();
                                while (reader.Read())
                                {
                                    jsonList.Add(reader["json_payload"].ToString());
                                }

                                // Convert the list of JSON strings to a single JSON array
                                string jsonArray = "[" + string.Join(",", jsonList) + "]";

                                // Display the JSON array
                                Console.WriteLine(jsonArray);
                            }
                            else
                            {
                                Console.WriteLine("No data found for client_id 'imdad'.");
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                }
            }

            return "";
        }

        public static string UpdateRetrieveDeviceSettings(string topics, string payload)
        {
            string[] _info = topics.Split('/');
            int rowsAffected = 0;
            string json_return = string.Empty;
            if (_info[2].Length > 0)
            {
                // Create a MySqlConnection object
                using (MySqlConnection connection = new MySqlConnection(connectionString))
                {
                    string qry = string.Empty;

                    try
                    {
                        // Open the connection
                        connection.Open();
                        qry = "UPDATE `AppDevices` SET `Connection`=@Connection WHERE `Name`=@Name;";

                        // Create a MySqlCommand object with the SQL statement and connection
                        using (MySqlCommand command = new MySqlCommand(qry, connection))
                        {
                            // Add parameters to the command

                            command.Parameters.AddWithValue("@Name", _info[2]);
                            command.Parameters.AddWithValue("@Connection", payload.Equals("connected") ? 1 : 0);

                            // Execute the command
                            rowsAffected = command.ExecuteNonQuery();

                            // Check if the insert was successful
                            Console.WriteLine(rowsAffected > 0 ? $"User {topics} Updated successfully." : "Failed to insert data.");

                            if (rowsAffected > 0)
                            {
                                qry = @"SELECT JSON_OBJECT('Id', Id, 'AccountId', AccountId, 'NAME', NAME, 'STATUS', STATUS, 
                                            'Temp', Temp, 'Door', Door, 'LDR', LDR, 'PIR', PIR, 'LDRAlertFreq', LDRAlertFreq, 
                                            'MinLDRAlert', MinLDRAlert, 'MinTempAlert', MinTempAlert,
                                            'TempAlertFreq', TempAlertFreq, 'CONNECTION', CONNECTION) AS json_payload FROM AppDevices 
                                            WHERE Name = @username";


                                // Create a MySqlCommand object with the SQL statement and connection
                                using (MySqlCommand command1 = new MySqlCommand(qry, connection))
                                {
                                    // Add parameter to the command
                                    command1.Parameters.AddWithValue("@username", _info[2]);
                                    //Execute the command
                                    using (MySqlDataReader reader = command1.ExecuteReader())
                                    {
                                        // Check if any rows were returned
                                        if (reader.HasRows)
                                        {
                                            // Read the rows and create a list of JSON strings
                                            List<string> jsonList = new List<string>();
                                            while (reader.Read())
                                            {
                                                jsonList.Add(reader["json_payload"].ToString());
                                            }

                                            // Convert the list of JSON strings to a single JSON array
                                            json_return = "[" + string.Join(",", jsonList) + "]";
                                            
                                            Console.WriteLine($"{json_return}");
                                            return json_return;
                                        }
                                        else
                                        {
                                            Console.WriteLine("No data found for client_id 'imdad'.");
                                        }
                                    }
                                }
                            }
                            return json_return;
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine("Error: " + ex.Message);
                        return json_return;
                    }
                }
            }
            return json_return;
        }
    }
}