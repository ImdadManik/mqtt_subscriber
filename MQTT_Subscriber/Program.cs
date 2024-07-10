using MQTTnet.Client;
using MQTTnet;
using MQTT_Subscriber;
using Org.BouncyCastle.Asn1;
using Newtonsoft.Json;

Random random = new Random();
int randomNumber = random.Next(0, 1000);

GenerateAES aes = new GenerateAES("098pub+1key+0pri", 256, "ABCXYZ123098");

string broker = "192.168.1.24"; //"http://192.168.1.135";// "e47dee11.emqx.cloud";
int port = 1883;
string clientId = string.Format("python-mqtt-{0}", randomNumber);
string topic_pir = "sensor/Pir/00000000daeca42f";
string topic_ldr = "sensor/Ldr/00000000daeca42f";
string topic_door = "sensor/Door/00000000daeca42f";
string topic_temp = "sensor/Temp/00000000daeca42f";

string username = "00000000daeca42f"; //"admin"; //"iotuser";
string password = aes.Encrypt("00000000daeca42f"); //"hash@123"; //"Fandaqah@2020";//"eqmx123!@#"; //"user@123"; 

string topic_heartbeat = "device/connected/" + username;

string prev_heartbeat = "disconnected";

try
{
    // Create a MQTT client factory
    var factory = new MqttFactory();

    // Create a MQTT client instance
    var mqttClient = factory.CreateMqttClient();

    // Create MQTT client options
    var options = new MqttClientOptionsBuilder()
        .WithTcpServer(broker, port) // MQTT broker address and port
        .WithCredentials(username, password) // Set username and password
        .WithClientId(clientId)
        .Build();

    mqttClient.ApplicationMessageReceivedAsync += (e) =>
    {
        if (e.ApplicationMessage.Topic.Equals(topic_heartbeat))
        {
            string curr_heartbeat = System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload);
            if (!string.IsNullOrEmpty(prev_heartbeat) && !String.IsNullOrEmpty(curr_heartbeat) && !curr_heartbeat.Equals(prev_heartbeat))
            {
                prev_heartbeat = curr_heartbeat;
                string jsonPayload = cMyDAL.UpdateRetrieveDeviceSettings(e.ApplicationMessage.Topic.ToString(), curr_heartbeat);

                cMsgPublisher.PublishMessage(jsonPayload, username, "device/" + username);
                cLog.WriteLog(jsonPayload);
            }
        }

        if (e.ApplicationMessage.Topic.Equals(topic_ldr))
        {
            string[] strings = e.ApplicationMessage.Topic.ToString().Split("/");
            emqx_msgs emqx = new emqx_msgs
            {
                CLIENTID = strings[2],
                MSGDATA = System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload),
                MSGTYPE = strings[1]
            };
            cLog.WriteLog(System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload));
            cMyDAL.addSensorDatas(e.ApplicationMessage.Topic.ToString(), emqx);
        }

        if (e.ApplicationMessage.Topic.Equals(topic_pir))
        {
            string[] strings = e.ApplicationMessage.Topic.ToString().Split("/");
            emqx_msgs emqx = new emqx_msgs
            {
                CLIENTID = strings[2],
                MSGDATA = System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload),
                MSGTYPE = strings[1]
            };

            cMyDAL.addSensorDatas(e.ApplicationMessage.Topic.ToString(), emqx);
        }

        if (e.ApplicationMessage.Topic.Equals(topic_temp))
        {
            string[] strings = e.ApplicationMessage.Topic.ToString().Split("/");
            emqx_msgs emqx = new emqx_msgs
            {
                CLIENTID = strings[2],
                MSGDATA = System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload),
                MSGTYPE = strings[1]
            };

            cMyDAL.addSensorDatas(e.ApplicationMessage.Topic.ToString(), emqx);
        }

        if (e.ApplicationMessage.Topic.Equals(topic_door))
        {
            string[] strings = e.ApplicationMessage.Topic.ToString().Split("/");
            emqx_msgs emqx = new emqx_msgs
            {
                CLIENTID = strings[2],
                MSGDATA = System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload),
                MSGTYPE = strings[1]
            };

            cMyDAL.addSensorDatas(e.ApplicationMessage.Topic.ToString(), emqx);
        }

        return Task.CompletedTask;
    };

    // Connect to MQTT broker
    var connectResult = await mqttClient.ConnectAsync(options);

    if (connectResult.ResultCode == MqttClientConnectResultCode.Success)
    {
        Console.WriteLine("Connected to MQTT broker successfully.");

        var topicsFilter_heartbeat = new MqttTopicFilterBuilder().WithTopic(topic_heartbeat).Build();
        var topicsFilter_ldr = new MqttTopicFilterBuilder().WithTopic(topic_ldr).Build();
        var topicsFilter_temp = new MqttTopicFilterBuilder().WithTopic(topic_temp).Build();
        var topicsFilter_pir = new MqttTopicFilterBuilder().WithTopic(topic_pir).Build();
        var topicsFilter_door = new MqttTopicFilterBuilder().WithTopic(topic_door).Build();

        await mqttClient.SubscribeAsync(topicsFilter_heartbeat);
        await mqttClient.SubscribeAsync(topicsFilter_ldr);
        await mqttClient.SubscribeAsync(topicsFilter_temp);
        await mqttClient.SubscribeAsync(topicsFilter_pir);
        await mqttClient.SubscribeAsync(topicsFilter_door);
        // Subscribe to a topic

        // Assign the message received event handler


        Console.ReadLine();

        // Disconnect from the MQTT broker
        await mqttClient.DisconnectAsync();

    }
    else
    {
        Console.WriteLine($"Failed to connect to MQTT broker: {connectResult.ResultCode}");
    }
}
catch (MQTTnet.Adapter.MqttConnectingFailedException ex)
{
    Console.Write(ex.Message);
}

