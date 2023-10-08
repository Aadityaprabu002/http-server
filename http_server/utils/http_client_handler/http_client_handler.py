from http_client.http_client import HttpClient
from http_router.http_router import HttpRouter, NoMatchingRouteException, NoMatchingTypeException
from http_request.http_request import HttpRequest
from http_response.http_response import HttpResponse
from socket import socket
from queue import Queue
from threading import Thread
import time

class HttpClientHandler:
    REQUEST_SIZE = 1024
    RESPONSE_TIME = 5
    def __init__(self,client_queue : Queue, request_router : HttpRouter):
        self._client_queue : Queue[HttpClient] = client_queue
        self._handler_queue :Queue[Thread] = Queue()
        self._allocator :[Thread] = None
        self._deallocator :[Thread] = None
        self._can_handle:[bool] = True
        self._can_deallocate:[bool] = True
        self.request_router = request_router


    def _handle(self,client_socket : socket):
        request = client_socket.recv(self.REQUEST_SIZE)
        request = HttpRequest(request.decode())
        response = ''
        try:
            response = str(self.request_router.handle(request))
            client_socket.send(response.encode())
        except NoMatchingRouteException:
            message = '<h1> 404 Not Found! <h1>'
            response = str(HttpResponse(message))
        except NoMatchingTypeException:
            message = '<h1> 403 Forbidden Request <h1>'
            response = str(HttpResponse(message))
             
        client_socket.send(response.encode())
        client_socket.close()
    
    def _allocate(self):
        try:
            while self._can_handle:
                while self._can_handle and not self._client_queue.empty():
                    client = self._client_queue.get()
                    handler = Thread(target = self._handle
                                     ,args=(client.client_socket,))
                    handler.start()
                    self._handler_queue.put(handler)
        except:
            print('Http client handler stopped due to some error')

    def _deallocate(self):
        try:
            while self._can_deallocate:
                while not self._handler_queue.empty():
                    handler = self._handler_queue.get()
                    if handler.is_alive():
                        time.sleep(self.RESPONSE_TIME)
                    handler.join()
        except:
            print('Handler deallocator stopped due to some error')
                

    def start(self):
        self._can_handle = True
        self._allocator = Thread(target = self._allocate)
        self._allocator.start()

        self._can_deallocate = False
        self._deallocator = Thread(target= self._deallocate)
        self._deallocator.start()

    def stop(self):
        self._can_handle = False

        while not self._client_queue.empty():
            client :[HttpClient] = self._client_queue.get()
            client.close()

        self._can_deallocate = False
        if self._allocator != None:
            self._allocator.join()
        if self._deallocator != None:
            self._deallocator.join()
    
        