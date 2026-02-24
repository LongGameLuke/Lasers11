import psycopg2
from typing import Union
from modules.consolelog import *

class PhotonDB:
    def __init__(self, dbname:str="photon"):
        self.dbname = dbname
        self.conn = None
        self.cur = None
    
    def connect_to_database(self) -> bool:
        try:
            # Connect to database and create cursor
            self.conn = psycopg2.connect(
                dbname=self.dbname
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
        return players
    
    def get_player_by_pid(self, pid:int):
        # Returns first player object from database with pid
        query = "SELECT * FROM players WHERE id = %s;"
        self.cur.execute(query, (pid,))
        player = self.cur.fetchone()
        return player

    def add_player(self, pid:int, player_name:str) -> bool:
        # Check if pid exists. If not, add player into database
        pid_test = self.get_player_by_pid(pid)
        if pid_test == None:
            self.cur.execute("INSERT into players(id, codename) VALUES (%s, %s)", (pid, player_name))
            self.conn.commit()
            log_process(f"Added {player_name} to database with id: {pid}")
            return True
        else:
           log_process(f"Found player with PID: {pid}")
        return False

    def remove_player(self, pid:int) -> bool:
        # Check if pid exists. If so, remove the entry
        pid_test = self.get_player_by_pid(pid)
        if pid_test != None and len(pid_test) >= 1:
            self.cur.execute("DELETE FROM players WHERE id = %s", (pid,))
            self.conn.commit()
            log_process(f"Removed player from database with id: {pid}")
            return True
        else:
            log_process(f"Couldn't find player with PID: {pid}")
            return False


# Database Menu
if __name__ == "__main__":
    db:Union[None, PhotonDB] = None
    while True:
        # Display menu and get user input
        print("\nPhoton Database Menu")
        print("=========================")
        print("1 = Connect to database")
        print("2 = Disconnect from database")
        print("3 = Display all players in database")
        print("4 = Search by PID")
        print("5 = Insert new player in database")
        print("6 = Remove player from database")
        print("7 = Exit")
        print("\nWhat to do?: ", end="")
        try:
            menu_choice:int = int(input())
            print("\n")
        except:
            print("Try again.")
            continue

        if menu_choice == 1:
            # Connect to database
            db = PhotonDB("photon")
            db.connect_to_database()
            print(f"Connected to database({db.dbname})")
        elif menu_choice == 2:
            # Disconnect from database
            try:
                db.disconnect_from_db()
            except Exception as e:
                print(e)
        elif menu_choice == 3:
            # Display all players in database
            players = db.get_all_players()
            for player in players:
                print(player)
        elif menu_choice == 4:
            # Search by PID
            try:
                pid:int = int(input("PID: "))
                db.get_player_by_pid(pid)
            except Exception as e:
                print(e)
        elif menu_choice == 5:
            # Insert new player in database
            pid = int(input("PID: "))
            player_name = input("Player Name: ")
            db.add_player(pid, player_name)
        elif menu_choice == 6:
            # Remove player from database
            pid = int(input("PID: "))
            db.remove_player(pid)
        elif menu_choice == 7:
            # Exit program
            exit(1) 
        else:
            continue
