import socket
from enum import Enum
from modules.consolelog import *

class TEAMS(Enum):
    NONE = ""
    GREEN = "Green"
    RED = "Red"

class SERVER_CODES(Enum):
    START = "202"
    END = "221"
    RED_BASE_HIT = "53"
    GREEN_BASE_HIT = "43"


class PhotonServer:
    def __init__(self, host:str, ports:dict):
        # Create PhotonServer object
        self.host = host
        self.broadcast_port = ports["broadcast"]
        self.receive_port = ports["receive"]
        self.bufferSize = 1024

        # Game status vars
        self.game_in_progress:bool = False
        self.players_tagged = 0

        # Datagram socket
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.udp_server_socket.bind((self.host, self.receive_port))

    def broadcast_message(self, message:str) -> None:
        # Sends a reply to client address
        encoded_message = str.encode(message)
        self.udp_server_socket.sendto(encoded_message, (self.host, self.broadcast_port))
    
    def start_game(self) -> None:
        # Send the start game code to clients
        log_process("Starting new game")
        start_code = str.encode(SERVER_CODES.START.value)
        self.game_in_progress = True
        self.udp_server_socket.sendto(start_code, (self.host, self.broadcast_port))

    def end_game(self) -> None:
        # Send the end game code to clients 3 times
        log_process("Ending current game")
        end_code = str.encode(SERVER_CODES.END.value)
        for i in range(3):
            self.udp_server_socket.sendto(end_code, (self.host, self.broadcast_port))
        self.game_in_progress = False

    def set_ports(self, broadcast:int, receive:int) -> None:
        # Sets current ports to new ones in event user changes them
        self.broadcast_port = broadcast
        self.receive_port = receive_port

    def update(self) -> None:
        # Update that runs every time the game updates
        bytesAddressPair = self.udp_server_socket.recvfrom(self.bufferSize)
        message = (bytesAddressPair[0]).decode()
        address = bytesAddressPair[1]
        clientMsg = f"Message from Client: {message}"
        clientIP  = f"Client IP Address: {address}"

        print(f"{clientIP}: {clientMsg}")

        self.players_tagged += 1
        hit_equipment = message.split(":")
        self.broadcast_message(hit_equipment[1])

        if self.players_tagged >= 6:
            self.end_game()