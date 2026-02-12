import yaml
from typing import Union
from modules.photondb import PhotonDB
from modules.photongame import PhotonGame
from modules.consolelog import *
from modules.photonserver import PhotonServer
from time import sleep

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
    print("\t\tLuke Fletcher")
    print("========================================\n")


def load_config(file_name:str) -> dict:
    # Load yaml data and return as a dict
    with open(file_name, "r") as file:
        try:
            log_process_start("Loading config")
            config:dict = yaml.safe_load(file)
            log_process_complete("Loaded config")
            return config
        except Exception as e:
            log_process_error("Couldn't load config. Check file integrity.", error=e)
            exit(-1)


def load_network_sockets(config:dict) -> dict:
    # Gather network sockets and return as a dict
    try:
        log_process_start("Loading network ports")
        broadcast_port = config["photon"]["network"]["broadcast-port"]
        receive_port = config["photon"]["network"]["receive-port"]
        ports:dict = {
            'broadcast': broadcast_port,
            'receive': receive_port
        }
        log_process_complete("Loaded network ports")
        return ports
    except Exception as e:
        log_process_error("Couldn't get networking ports. Check file integrity.", error=e)
        exit(-1)


def load_database(config:dict) -> PhotonDB:
    # Connect to the postgresql database
    try:
        log_process_start("Connecting to database")
        db = PhotonDB(
            host=config["database"]["host"],
            port=config["database"]["port"],
            user=config["database"]["user"],
            password=config["database"]["password"],
            dbname=config["database"]["db-name"]
            )
        db.connect_to_database()
        log_process_complete("Connected to database")
        return db
    except Exception as e:
        log_process_error("Couldn't connect to postgresql database.", e)
        exit(-1)


if __name__ == "__main__":
    # Display welcome message to user on command line
    start_message()

    # Load config
    config:dict = load_config(CONFIG_FILE)

    # Load network ports from config
    ports = load_network_sockets(config)

    # Load database connection
    db = load_database(config)
    
    # Create game server
    log_process_start("Creating game server")
    server = PhotonServer(config["photon"]["network"]["host"], ports)
    log_process_complete("Created game server")
    print("\n")
    log_process(f"Server listening on port {ports['receive']}/udp")
    log_process(f"Server broadcasting on port {ports['broadcast']}/udp")
    print("\nPress Ctrl+c to exit program.\n")

    # Create game using initialized data
    game = PhotonGame(db, server)

    # Start game
    server.start_game()

    # Main program loop
    keep_running = True
    while keep_running:
        try:
            keep_running = game.update()
        except KeyboardInterrupt:
            keep_running = False
    
    # Exit program after loop broken
    db.disconnect_from_db()
    print("\n\nGoodbye.")
    exit(1)