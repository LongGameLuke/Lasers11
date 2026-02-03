import socket

class PhotonServer:
    def __init__(self, host:str, ports:dict):
        self.host = host
        self.broadcast_port = ports["broadcast"]
        self.receive_port = ports["receive"]
        self.bufferSize = 1024
        self.msgFromServer = "Hello UDP Client"
        self.bytesToSend = str.encode(self.msgFromServer)

        # Datagram socket
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.udp_server_socket.bind((self.host, self.receive_port))

    def send_message(self, reply_address:str):
        # Sends a reply to client address
        self.udp_server_socket.sendto(self.bytesToSend, reply_address)

    def update(self):
        bytesAddressPair = self.udp_server_socket.recvfrom(self.bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        print(f"{clientIP}: {clientMsg}")
        self.send_message(address)