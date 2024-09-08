import psycopg2
import os
class POSTGRESQL:
    """
    Note:
        ポスグレに接続できるpsycopg2を自分なりにラッパーしたやつ
    """
    def __init__(self) -> None:
        self._host = ''
        self._user = ''
        self._password = 'password'
        self._database = ''
        self._db_connection = None
    

    def setting_connection(self,host:str,user:str,password:str,database:str):
        """
        Args:
            host : ipアドレス
            user : 接続するポスグレのユーザーネーム
            password : 接続するポスグレのパスワード
            database : 接続するDBの名前
        """
        self._host = host
        self._user = user
        self._password = password
        self._database = database
    
    def connect_DB(self):
        """
        Note : ポスグレに接続するやつ setting_connectionの後に実行,
               connect DB 〇〇と出ればOK
        """
        self._db_connection = psycopg2.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database 
        )
        print("connect DB {}".format(self._database))
    
    def exec_update(self,query:str):
        """
        Args:
            query : クエリ文をそのままいれる(str)
        Note: 
            元あるデータを更新する用の実行関数(insertとかupdateとか)。戻り値なし.
        """
        with self._db_connection:
            with self._db_connection.cursor() as cursor:
                cursor.execute(query=query)
            self._db_connection.commit()
        cursor.close()
    
    def exec_select(self,query:str):
        """
        Args:
            query : クエリ文をそのままいれる(str)
        Note: 
            名前の通りselectする用のやつ。戻り値あり、タプル型で返ってくる
        """
        retV = None
        with self._db_connection:
            with self._db_connection.cursor() as cursor:
                cursor.execute(query=query)
                retV = cursor.fetchall()
            self._db_connection.commit()
        cursor.close()
        return retV
    

if __name__ == "__main__":
    # インスタンス作成
    DB = POSTGRESQL()
    # DBに接続するための設定
    DB.setting_connection(host='10.77.114.51',user='postgres',database='mytable')
    # DBに接続
    DB.connect_DB()
    # select実行(以下はdata_bridgeというテーブルから全ての情報を引き出す)
    a=DB.exec_select('select * from data_bridge')
    print(a)
    # update実行 (data_bridgeテーブルのvalueというデータがTrueならFalseに書き換える)
    DB.exec_update("UPDATE data_bridge SET value = 'False' where value='True'")
    a=DB.exec_select('select * from data_bridge')
    print(a)

