from postgresql import POSTGRESQL

if __name__ == "__main__":
    DB = POSTGRESQL()
    DB.setting_connection(host="192.168.11.2",user='postgres',database='test')
    DB.connect_DB()
    a = DB.exec_select('select * from sensor_data;')
    print(a)