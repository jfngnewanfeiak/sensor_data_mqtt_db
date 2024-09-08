from paho.mqtt import client as mqtt
from socket import gethostname,gethostbyname

# ip取得
your_ip = gethostbyname(gethostname())
#コメントを追加
class MQTT_PUB:
    """
    Note:
        使い方
        0 インスタンス生成
        1 pub_con()実行
        2 pubmsg_setter()でmsg変更
        3 任意のタイミングでpub_run()実行
        4 2,3を使っていく。
    """
    def __init__(self) -> None:
        self.broker = ""
        self.port = 1883
        self.topic = ""
        self.pubmsg = ""
        self.username = ""
        self.password = "password"
        self.client = None
        
    def __broker_setter(self,broker_ip:str):
        self.broker = broker_ip
    
    def __topic_setter(self,topic_name:str):
        self.topic = topic_name
    
    def pubmsg_setter(self,pubmsg):
        """
        Args:
            pubmsg: publishするデータ(str)
        Note:
            publishするデータを設定するための関数
        """
        self.pubmsg = pubmsg
    
    def __connect_mqtt(self)->mqtt:
        def __on_connect(client,ud,flag,rc):
            if rc == 0:
                print("Connected to Mqtt Broker")
            else:
                print("Failed to connect mqtt broker")
        
        client = mqtt.Client()
        client.username_pw_set(self.username,self.password)
        client.on_connect = __on_connect
        client.connect(self.broker,self.port)
        return client
    
    
    def pub_con(self,broker_ip:str,topic_name:str,pubmsg:str,port=1883)->mqtt:
        """
        Args:
            broker_ip: mqttブローカのipアドレスもしくはbroker.emqx.io
            topic_name: mqtt通信用のトピック名
            pubmsg: publishするメッセージ(str)
            port: mqtt通信のポート。デフォルト値 1883
        """
        def __on_connect(client,userdata,flag,rc):
            if rc == 0:
                print("Connected to Mqtt Broker")
            else:
                print("Failed to connect mqtt broker")
            
        # 設定
        self.__broker_setter(broker_ip=broker_ip)
        self.__topic_setter(topic_name=topic_name)
        self.pubmsg_setter(pubmsg=pubmsg)
        self.port = port
        self.client = mqtt.Client()
        self.client.username_pw_set(self.username,self.password)
        self.client.on_connect = __on_connect
        self.client.connect(self.broker,self.port)
        return self.client
    
    def pub_run(self):
        result = self.client.publish(self.topic,self.pubmsg)

        status = result[0]

        if status == 0:
            print(f"Send `{self.pubmsg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send msg to topic {self.topic}")


if __name__ == "__main__":
    mqtt_PUBLISHER = MQTT_PUB()
    mqtt_PUBLISHER.pub_con(broker_ip=your_ip,topic_name="req/manage",pubmsg="Hello mqtt World!")
    
    mqtt_PUBLISHER.pub_run()
    #mqtt_PUBLISHER.pubmsg_setter("変えてみた")
    #mqtt_PUBLISHER.pub_run()
    