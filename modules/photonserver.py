import socket
from enum import Enum
from modules.consolelog import *

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

        # Ref to game that is set after game is created
        self.game = None

        # Datagram socket
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.udp_server_socket.bind((self.host, self.receive_port))


    def broadcast_message(self, message:str) -> None:
        # Broadcasts a message to all clients
        encoded_message = str.encode(message)
        self.udp_server_socket.sendto(encoded_message, (self.host, self.broadcast_port))
    

    def start_game(self) -> None:
        # Send the start game code to clients
        log_process(f"Starting new game with {len(self.game.players)} players!")
        start_code = str.encode(SERVER_CODES.START.value)
        self.udp_server_socket.sendto(start_code, (self.host, self.broadcast_port))


    def end_game(self) -> None:
        # Send the end game code to clients 3 times
        log_process("Ending current game")
        end_code = str.encode(SERVER_CODES.END.value)
        for i in range(3):
            self.udp_server_socket.sendto(end_code, (self.host, self.broadcast_port))


    def set_ports(self, broadcast:int, receive:int) -> None:
        # Sets current ports to new ones in event user changes them
        self.broadcast_port = broadcast
        self.receive_port = receive_port


    def event_player_tag(self, equipment_tagger:int, equipment_tagged:int):
        tagger = None
        tagged_player = None

        # Find player profile assosiated with equipment ids
        for player in self.game.players:
            if player.equipment_id == equipment_tagger:
                tagger = player
            elif player.equipment_id == equipment_tagged:
                tagged_player = player
            
            # Exit for loop if profiles are found
            if tagger != None and tagged_player != None:
                continue
        
        # Let PhotonGame handle game logic
        self.game.player_tagged(tagger, tagged_player)

    
    def broadcast_tagged(self):
        # Broadcast the tagged signal to equipment that needs to "shut down"
        self.broadcast_message(hit_equipment[1])


    def update(self) -> None:
        # Update that runs every time the game updates
        bytesAddressPair = self.udp_server_socket.recvfrom(self.bufferSize)
        message = (bytesAddressPair[0]).decode()
        address = bytesAddressPair[1]
        clientMsg = f"Message from Client: {message}"
        clientIP  = f"Client IP Address: {address}"

        print(f"{clientIP}: {clientMsg}")

        hit_equipment = message.split(":")
        self.event_player_tag(hit_equipment[0], hit_equipment[1])