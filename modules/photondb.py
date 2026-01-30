import psycopg2
from typing import Union
from getpass import getpass # replacement for input() when inputting passwords

class PhotonDB:
    def __init__(self, user:str, password:str, host:str="127.0.0.1", port:int=5432, dbname:str="photon"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = None
        self.cur = None
    
    def connect_to_database(self) -> bool:
        try:
            # Connect to database and create cursor
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            raise e

    def disconnect_from_db(self) -> bool:
        # Disconnect from database
        try:
            self.conn.close()
            self.cur.close()
            return True
        except Exception as e:
            raise e
            return False

    def get_all_players(self) -> dict:
        query = "SELECT * FROM players"
        self.cur.execute(query)
        players = self.cur.fetchall()
        print(players)
        return players
    
    def get_player_by_pid(self, pid:int):
        # Returns first player object from database with pid
        query = "SELECT * FROM players WHERE id = %s;"
        self.cur.execute(query, (pid,))
        player = self.cur.fetchone()
        return player


# Database Menu
if __name__ == "__main__":
    db:Union[None, PhotonDB] = None
    while True:
        print("\nPhoton Database Menu")
        print("=========================")
        print("1 = Connect to database")
        print("2 = Disconnect from database")
        print("3 = Display all players in database")
        print("4 = Search by PID")
        print("5 = Exit")
        print("\nWhat to do?: ", end="")
        try:
            menu_choice:int = int(input())
        except:
            print("Try again.")
            continue

        if menu_choice == 1:
            username = input("Database Username: ")
            password = getpass("Database Password: ")
            db = PhotonDB(user=username, password=password)
            db.connect_to_database()
            print(f"Connected to database({db.dbname})")
        elif menu_choice == 2:
            try:
                db.disconnect_from_db()
            except Exception as e:
                print(e)
        elif menu_choice == 3:
            pass
        elif menu_choice == 4:
            try:
                pid:int = int(input("PID: "))
            except Exception as e:
                print(e)
        elif menu_choice == 5:
            exit(1) 
        else:
            continue
