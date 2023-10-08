from socket import socket
class HttpClient:
    def __init__(self,client_socket :socket, client_address: tuple):
        assert len(client_address) == 2, 'Client address should contain only ipaddress and port'
        self.client_socket = client_socket
        self.client_ip_address = client_address[0]
        self.client_port = client_address[1]
    def close(self):
        self.client_socket.close()
