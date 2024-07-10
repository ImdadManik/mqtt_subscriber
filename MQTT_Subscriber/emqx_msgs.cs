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
}
