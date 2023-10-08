class HttpRequest:
    def __init__(self,request : str):
        print(request)
        self.request = request.split('\n')
        request_line = self.request[0].split(' ')
        self.request_type = request_line[0]
        self.request_path = request_line[1]