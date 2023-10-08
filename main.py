from http_server.http_server import HttpServer
from http_response.http_response import HttpResponse

def index():
    content = ''
    with open('index.html') as file:
        content = file.read()
    response =  HttpResponse(content)
    return response
def iphone():
    content = ''
    with open('iphone.html') as file:
        content = file.read()
    response =  HttpResponse(content)
    return response

if __name__ == "__main__":
    app = HttpServer(9999)
    app.request_router.map_get('/index',index)
    app.request_router.map_get('/apple/iphone',iphone)
    app.listen()
    
