from abc import ABC, abstractmethod
import multiprocessing
from http_data_parser import RequestParser

class BaseHandler(ABC):
    DEFAULT_READ_SIZE = 1024
    DEFAULT_WRITE_SIZE = 1024

    def read(self, size = None):
        size = size if size else self.DEFAULT_READ_SIZE
        return self._sock.recv(size)

    def read_all(self):
        result = bytes()
        for temp in iter(self.read, b''):
            result += temp
            if len(temp) < self.DEFAULT_READ_SIZE:
                break
        return result

    def read_in_chunk(self, func, size = None):
        size = size if size else self.DEFAULT_READ_SIZE
        for temp in iter(self.read, b''):
            func(temp)
            if len(temp) < size:
                break

    def write(self, data):
        if data:
            self._sock.sendall(data)

    def write_in_stream(self, iterators):
        for data in iter(iterators):
            self.write(data)

    def write_data_in_stream(self, data, size = None):
        size = size if size else self.DEFAULT_WRITE_SIZE
        def stream():
            length = len(data)
            index = 0
            while index < length:
                index += size
                yield data[index - size, index]

        self.write_in_stream(stream())

    def do_with(self, sock):
        self._sock = sock
        self.handle()

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
        header = "HTTP/1.1 200 OK\r\nDate: Fri, 14 Oct 2016 09:10:42 GMT\r\nContent-Type: text/plain\r\n\r\n"
        req = RequestParser(self.read_all())
        res = str('\n'.join(list([name + ':' + value for name, value in req.headers])))
        self.write((header+res).encode('ascii'))   
    