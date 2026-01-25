import psycopg2

class PhotonDB:
    def __init__(self, user:str, password:str, host:str="127.0.0.1", port:int=5432, dbname:str="players"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = None
        self.cur = None
    
    def connect_to_database(self):
        try:
            # Connect and create cursor
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            raise e

    def disconnect_from_db(self) -> bool:
        try:
            self.conn.close()
            self.cur.close()
            return True
        except Exception as e:
            print(e)
            return False