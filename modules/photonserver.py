import socket
from enum import Enum
from modules.consolelog import *
import time

class SERVER_CODES(Enum):
    START = "202"
    END = "221"
    RED_BASE_HIT = "53"
    GREEN_BASE_HIT = "43"


class PhotonServer:
    def __init__(self, host:str, ports:dict, game):
        # Create PhotonServer object
        self.host = host
        self.broadcast_port = ports["broadcast"]
        self.receive_port = ports["receive"]
        self.bufferSize = 1024

        # Ref to parent Photongame
        self.game = game

        # Set up sockets
        self.udp_receive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.start_sockets()

    def start_sockets(self):
        # Sets up server network and binds system ports
        self.udp_receive.settimeout(1)  # Program will hang if there is no timeout
        self.udp_receive.bind((self.host, self.receive_port))
        self.log_current_ports()
    
    def log_current_ports(self):
        # Displays current server ports in console
        log_process(f"Server listening on port {self.receive_port}/udp")
        log_process(f"Server broadcasting on port {self.broadcast_port}/udp")

    def broadcast_message(self, message:str) -> None:
        # Broadcasts a message to all clients
        encoded_message = str.encode(message)
        log_game_event(f"Broadcast: '{message}'")
        self.udp_broadcast.sendto(encoded_message, (self.host, self.broadcast_port))

    def start_game(self) -> None:
        # Send the start game code to clients
        log_process(f"Starting new game with {len(self.game.players)} players!")
        self.broadcast_message(SERVER_CODES.START.value)

    def end_game(self) -> None:
        # Send the end game code to clients 3 times
        log_process("Ending current game")
        for i in range(3):
            self.broadcast_message(SERVER_CODES.END.value)

    def set_network(self, host=None, broadcast=None, receive=None) -> None:
        # Sets current ports & host to new ones in event user changes them
        # Close old netowrk binds
        self.udp_receive.close()
        self.udp_receive.close()
        # Load new network info
        if broadcast != None:
            self.broadcast_port = broadcast
        if receive != None:
             self.receive_port = receive
        if host != None:
             self.host = host
        # Start sockets with new host/ports
        self.udp_receive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.start_sockets()

    def event_player_tag(self, equipment_tagger:int, equipment_tagged:int):
        tagger = None
        tagged = None

        # Find player profile assosiated with equipment ids
        for player in self.game.players:
            if player.equipment_id == equipment_tagger:
                tagger = player
            elif player.equipment_id == equipment_tagged:
                tagged = player
            
            # Exit for loop if profiles are found
            if tagger != None and tagged != None:
                continue
        
        # Let PhotonGame handle game logic
        self.game.event_player_tag(tagger, tagged)

    def event_base_tag(self, equipment_tagger:int, base_code:int):
        tagger = None

        # Find player profile assosiated with equipment ids
        for player in self.game.players:
            if player.equipment_id == equipment_tagger:
                tagger = player
            
            # Exit for loop if profile is found
            if tagger != None:
                continue
            
        # Let PhotonGame handle game logic
        self.game.event_base_tag(tagger, base_code)

    def broadcast_tagged(self, equipment_id:int):
        # Broadcast the tagged signal to equipment that needs to "shut down"
        # This is kinda a silly method to have
        self.broadcast_message(str(equipment_id))

    def update(self) -> None:
        # Update that runs every time the game updates
        try:
            # Gather udp data from receive port
            bytesAddressPair = self.udp_receive.recvfrom(self.bufferSize)
            message = (bytesAddressPair[0]).decode()
            address = bytesAddressPair[1]

            # Split received data
            hit_equipment = message.split(":")

            # Determine if base or player tag
            if hit_equipment[1] == SERVER_CODES.RED_BASE_HIT.value or hit_equipment[1] == SERVER_CODES.GREEN_BASE_HIT.value:
                self.event_base_tag(int(hit_equipment[0]), int(hit_equipment[1]))
            else:
                self.event_player_tag(int(hit_equipment[0]), int(hit_equipment[1]))
        except:
            # do nothing when udp timeout
            pass