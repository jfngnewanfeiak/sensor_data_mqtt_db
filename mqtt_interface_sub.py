from paho.mqtt import client as mqtt
from socket import gethostname,gethostbyname

# ip取得
your_ip = gethostbyname(gethostname())

class MQTT_SUB:
    """
    Note:
        使い方
        0 インスタンス生成
        1 sub_run()実行。
    """
    def __init__(self) -> None:
        self.__broker = ""
        self.__port = 1883 #default settings
        self.__topic = ""
        self.__username = "user"
        self.__password = "password"
        self.__callback = None

    # セッター
    def borker_setter(self,broker_ip:str):
        self.__broker = broker_ip
    
    def topic_setter(self,topic_name:str):
        self.__topic = topic_name
    
    def _port_setter(self,port:int):
        self.__port = port
    
    # ブローカに接続
    def __connect_mqtt(self)->mqtt:
        def __on_connect(client,ud,flag,rc):
            if rc == 0:
                print("Connected to Mqtt Broker")
            else:
                print("Failed to connect mqtt broker")
        
        client = mqtt.Client()
        client.username_pw_set(self.__username,self.__password)
        client.on_connect = __on_connect
        client.connect(self.__broker,self.__port)
        
        return client


    def __subscribe(self,client:mqtt):
        def __on_message(client,ud,msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.__callback(msg.payload.decode())
            # self.__callback()
        
        client.subscribe(self.__topic)
        client.on_message = __on_message
    
        
    def sub_run(self,broker_ip:str,topic_name:str,cb,port=1883):
        """
        Args:
            broker_ip: mqttブローカのipアドレス
            topic_name: mqtt通信するための自分が決めたトピックの名前
            cb: データを受け取った後に実行する関数。第一引数に受け取ったデータが入る
            port: mqtt通信するためのポート番号を指定。デフォルト値は1883。自分でファイヤーウォール設定したやつ
        Note:
            topicを受け取るようにするための実行関数
        """
        # 設定
        self.borker_setter(broker_ip=broker_ip)
        self.topic_setter(topic_name=topic_name)
        self._port_setter(port=port)


        client = self.__connect_mqtt()
        self.__subscribe(client=client)
        self.__callback = cb
        # client.loop_start()
        client.loop_forever()

        
    def callback(self):
        print("callback")


if __name__ == "__main__":
    mqtt_SUBSCRIBER = MQTT_SUB()
    # ここは引数に合わせて設定
    mqtt_SUBSCRIBER.sub_run(broker_ip=your_ip,topic_name="req/manage",cb=mqtt_SUBSCRIBER.callback)

