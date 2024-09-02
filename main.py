import sys
from os import environ
import time
#import smbus
from mqtt_interface_pub import MQTT_PUB
from mqtt_interface_sub import MQTT_SUB
# i2c = smbus.SMBus(1)
from postgresql import POSTGRESQL

sensor_address = 0x5c

# def wake_up_sensor(address):
#     try:
#         i2c.write_i2c_block_data(address,0x00,[])
#     except:
#         pass

# def read_temperature_humidity(address):
#     i2c.write_i2c_block_data(address,0x03,[0x00,0x04])
#     time.sleep(0.015)
#     return i2c.read_i2c_block_data(address,0,6)

def callback(msg):
    print(msg)

if __name__ == "__main__":
    # mqtt settings
    # pub = MQTT_PUB()
    # pub.pub_con(broker_ip="broker.emqx.io",topic_name='desktop_mqtt',pubmsg="hoge")
    DB = POSTGRESQL()
    DB.setting_connection(host='192.168.2.161',user='postgres',password=environ.get('MYPASSWORD'),database='sensor_db')
    DB.connect_DB()
    print('connect!!!')
    # sub = MQTT_SUB()
    # sub.sub_run(broker_ip='broker.emqx.io',topic_name='topic/AM2320',cb=callback)
    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     exit()