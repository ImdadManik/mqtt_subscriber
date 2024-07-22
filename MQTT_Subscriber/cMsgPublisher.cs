using MQTTnet;
using MQTTnet.Client;
using System;

namespace MQTT_Subscriber
{
    public static class cMsgPublisher
    {
        public static void PublishMessage(string _payload, string _username, string _topics)
        {
            Random random = new Random();

            int randomNumber = random.Next(1000, 1000000);
            GenerateAES aes = new GenerateAES("098pub+1key+0pri", 256, "ABCXYZ123098");

            string broker = "pms-db003.fandaqah.com"; // "192.168.1.24"; //"http://192.168.1.135";// "e47dee11.emqx.cloud";
            int port = 1883;
            string clientId = string.Format("python-mqtt-{0}", randomNumber);
            string topic = _topics;
            string username = _username; //"saqib";// "00000000daeca42f";
            string password = aes.Encrypt(_username);
            var factory = new MqttFactory();

            // Create a MQTT client instance
            var mqttClient = factory.CreateMqttClient();

            // Create MQTT client options
            var options = new MqttClientOptionsBuilder()
                .WithTcpServer(broker, port) // MQTT broker address and port
                .WithCredentials(username, password) // Set username and password
                .WithClientId(clientId)
                .Build();

            try
            {
                // Connect to MQTT broker
                var connectResult = mqttClient.ConnectAsync(options).GetAwaiter().GetResult();
                if (connectResult.ResultCode == MqttClientConnectResultCode.Success)
                {
                    Console.WriteLine("Connected to MQTT broker successfully.");
                    var mqttMessage = new MqttApplicationMessageBuilder()
                                    .WithTopic(topic)
                                    .WithPayload(_payload)
                                    .WithRetainFlag()
                                    .WithQualityOfServiceLevel(MQTTnet.Protocol.MqttQualityOfServiceLevel.AtMostOnce)
                                    .Build();  

                    mqttClient.PublishAsync(mqttMessage).GetAwaiter().GetResult();

                    // Disconnect from the MQTT broker
                    mqttClient.DisconnectAsync().GetAwaiter().GetResult();
                }
                else
                {
                    Console.WriteLine($"Failed to connect to MQTT broker: {connectResult.ResultCode}");
                }
            }
            catch (MQTTnet.Adapter.MqttConnectingFailedException ex)
            {
                Console.WriteLine($"Failed to connect to MQTT broker due to exception: {ex.Message}");
            }
        }

    }
}
