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

# Database Menu
if __name__ == "__main__":
    while True:
        print("\nPhoton Database Menu")
        print("=========================")
        print("1 = Connect to database")
        print("2 = Disconnect to database")
        print("4 = Exit")
        print("\nWhat to do?: ", end="")
        try:
            menu_choice:int = int(input())
        except:
            print("Try again.")
            continue

        if menu_choice == 1:
            pass
        elif menu_choice == 2:
            pass
        elif menu_choice == 4:
            exit(1) 
        else:
            continue
