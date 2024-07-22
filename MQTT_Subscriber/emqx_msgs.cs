using MySqlX.XDevAPI;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MQTT_Subscriber
{
    public class emqx_msgs
    {
        public string CLIENTID { get; set; }
        public string MSGDATA { get; set; }
        public string MSGTYPE { get; set; }
    }

    public class device_status
    {
        public string USER_NAME { get; set; }
        public string STATUS { get; set; }
    }

    public class heart_beat
    {
        public string IsConnected { get; set; }
        public string AccountId { get; set; }
        public string Id { get; set; }
    }

    public class SensorPayload
    {
        public string Id { get; set; }
        public string NAME { get; set; }
        public string AccountId { get; set; }
        public bool LDR { get; set; }
        public bool PIR { get; set; }
        public bool Door { get; set; }
        public bool Temp { get; set; }
        public bool DeviceStatus { get; set; }
        public bool AccountStatus { get; set; }
        public bool CONNECTION { get; set; }
        public int MinLDRAlert { get; set; }
        public int LDRAlertFreq { get; set; }
        public int MinTempAlert { get; set; }
        public int TempAlertFreq { get; set; }
    }

}
