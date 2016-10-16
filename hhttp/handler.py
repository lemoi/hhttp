from abc import ABC, abstractmethod
import multiprocessing
from .http_data_parser import RequestHeaderParser, ResponseHeaderGenerator
from .sock_warpper import SockWarpper

class BaseHandler(ABC):

    def do_with(self, sock):
        self.sw = SockWarpper(sock)
        self.req = RequestHeaderParser(self.get_header_data())
        self.handle()

    def get_header_data(self):
        return self.sw.read_header_data()
    
    def get_body_data(self, target = None):
        return self.sw.read_body_data(target)

    def send_header_data(self, data):
        self.sw.write(data)

    def send_body_data(self, data = None, stream = None):
        if not self.sw._write_buffer:
            raise Exception('the header has not set')
        self.sw.flush()
        if data != None:
            self.sw.write(data)
            self.sw.flush()
        elif stream:
            self.sw.write_in_stream(stream)
        else:
            raise Exception('there must be at least one param') 

    @abstractmethod   
    def handle(self):
        """deal with """

class WSGIHandler(BaseHandler):
    """
    wsgi:

    application(environ, start_response)
    start_response(status, response_headers[, exc_info])
        status: eg: "200 OK"
        response_headers: [(header_name, header_value), ()]
        exc_info: It is used only when the application has trapped an error and is attempting to display an error message to the browser.
    """
    def __init__(self, application_path = None):
        # import importlib
        # self.application = importlib.import_module(application_path)#多进程缺陷
        pass
    def handle(self):
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
        req = RequestHeaderParser(self.get_header_data())
        print('header parse finish')
        environ = req.to_cgi_environ()
        environ['wsgi.version'] = (1, 0)
        res = str('\n'.join(list([name + ':' + str(value) for name, value in environ.items()])))
        self.sw.write((header+res).encode('ascii'))
        self.sw.flush()

class StaticFileHandler(BaseHandler):
    def __init__(self):
        from .consts import CONFIG_PARAM
        self.root = CONFIG_PARAM['root']

    def handle(self):
        from .consts import MIME_TYPES
        import os.path as pathlib
        path = pathlib.join(self.root, self.req.req_path[1:])
        print(path)
        if pathlib.isfile(path):
            res = ResponseHeaderGenerator(200)
            ext = path[path.rfind('.')+1:]
            res['content-type'] = MIME_TYPES[ext]
            self.send_header_data(res.to_bytes())
            with open(path, 'rb') as fp:
                if pathlib.getsize(path) > 1024 * 1024:
                    def rd():
                        while True:
                            data = fp.read(1024)
                            if not data:
                                break
                            yield data
                    self.send_body_data(stream = rd())
                else:
                    self.send_body_data(fp.read())
        else:
            res = ResponseHeaderGenerator(404)
            self.send_header_data(res.to_bytes())
            self.send_body_data('')