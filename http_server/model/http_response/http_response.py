class HttpResponse:
    def __init__(self,response : str):
        self.response_body = response
        self.response_start = 'HTTP/1.0 200 OK'
        self.response_header = f''' 
Content-type: text/html
Content-length: {len(response)}'''
    def __str__(self):
        return f'{self.response_start}{self.response_header}\n\n{self.response_body}'