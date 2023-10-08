from http_request.http_request import HttpRequest
class NoMatchingRouteException(Exception):
    def __init__(self,route):
        message = f'{route} not present in the route map!'
        super().__init__(message)

class NoMatchingTypeException(Exception):
    def __init__(self,type):
        message = f'{type} not present in route map!'
        super().__init__(message)


class HttpRouter:
    def __init__(self):
        self._route_map = dict()
        self._route_map['GET'] = dict()
        self._route_map['POST'] = dict()
        self._route_map['PUT'] = dict()
        self._route_map['DELETE'] = dict()
      
    def map_get(self,route:str,callback):
        self._route_map['GET'][route] = callback
    def map_post(self,route,callback):
        self._route_map['POST'][route] = callback
    def map_put(self,route,callback):
        self._route_map['PUT'][route] = callback
    def map_delete(self,route,callback):
        self._route_map['DELETE'][route] = callback

    def handle(self,request : HttpRequest):
    
        if request.request_type in self._route_map:
            if request.request_path in self._route_map[request.request_type]:
                return self._route_map[request.request_type][request.request_path]()
            else:
                raise NoMatchingRouteException(request.request_path)
        else:
            raise NoMatchingTypeException(request.request_type)
