from http_client_handler.http_client_handler import HttpClientHandler
from http_client.http_client import HttpClient
from http_router.http_router import HttpRouter
from queue import Queue
import socket
class HttpServer:
    def __init__(self, port):
        self._server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server_port = port
        self._client_queue = Queue(maxsize=10)
        self.request_router = HttpRouter()
        self._client_handler = HttpClientHandler(client_queue=self._client_queue, 
                                                 request_router = self.request_router)
        self._server_up = True
        
        try:
            self._server_socket.bind(('',self._server_port))
            self._client_handler.start()
            
        except socket.error as e:
            print( f'Failed to bind server to port: {self._server_port}')
            self.close()
    

    def listen(self):
        client:[HttpClient] = None
        try:
            self._server_socket.listen()
            while self._server_up:
                incoming = self._server_socket.accept()
                client = HttpClient(incoming[0],incoming[1])
                self._client_queue.put(client)
        except:
           print('Error during listening to clients')
           self.close()
           
    def close(self):
        print('Server shutting down')
        self._server_up = False
        self._client_handler.stop()
        self._server_socket.close()