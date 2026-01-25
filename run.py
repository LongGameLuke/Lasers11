import yaml
from typing import Union
from modules.photondb import PhotonDB
from modules.consolelog import *

CONFIG_FILE = "config.yaml"

def start_message() -> None:
    print("""    ____  __          __            
   ╱ __ ╲╱ ╱_  ____  ╱ ╱_____  ____ 
  ╱ ╱_╱ ╱ __ ╲╱ __ ╲╱ __╱ __ ╲╱ __ ╲
 ╱ ____╱ ╱ ╱ ╱ ╱_╱ ╱ ╱_╱ ╱_╱ ╱ ╱ ╱ ╱
╱_╱   ╱_╱ ╱_╱╲____╱╲__╱╲____╱_╱ ╱_╱ 
                                    """)
    print("Welcome to Photon Laser Tag.")
    print("========================================")
    print("\tCreated by Team 11:")
    print("\t\tDayo Arigbede")
    print("\t\tBrendyn Burgess")
    print("\t\tBrad Chailland")
    print("\t\tAngel Duron")
    print("\t\tLuke Fletcher")
    print("========================================\n")

def load_config(file_name:str) -> dict:
    # Load yaml data
    with open(file_name, "r") as file:
        try:
            data = yaml.safe_load(file)
            return data
        except Exception as e:
            raise e

if __name__ == "__main__":
    # Display welcome message to user on command line
    start_message()

    # Load config
    config:Union[None, dict] = None
    try:
        log_process_start("Loading config")
        config = load_config(CONFIG_FILE)
        log_process_complete("Loaded config")
    except Exception as e:
        log_process_error("Couldn't load config. Check file integrity.", error=e)
        exit(-1)

    # Connect to the postgresql database
    try:
        log_process_start("Connecting to database")
        db = PhotonDB(
            host=config["database"]["host"],
            port=config["database"]["port"],
            user=config["database"]["user"],
            password=config["database"]["password"]
            )
        db.connect_to_database()
        log_process_complete("Connected to database")
    except Exception as e:
        log_process_error("Couldn't connect to postgresql database.")
        exit(-1)

    # TODO: Launch GUI

    # Wait for input and close program
    print("\nPress ENTER to close program.", end="")
    input()
    exit(1)