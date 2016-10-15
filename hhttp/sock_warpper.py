class ReadError():
    pass
class SockWarpper:
    DEFAULT_READ_SIZE = 1024
    DEFAULT_WRITE_SIZE = 1024
    HTTP_HEAD_BODY_SEP = b'\r\n\r\n'
    def __init__(self, sock):
        self._sock = sock
        self._read_buffer = bytes()
        self._write_buffer = bytes()
        self._readable = True

    def read(self, size = None):
        size = size if size else self.DEFAULT_READ_SIZE
        data = self._sock.recv(size)
        if len(data) < size:
            self._readable = False
        return data

    def read_all(self):
        result = bytes()
        while self._readable:
            temp = self.read()
            result += temp
        return result

    def read_header_data(self):
        result = bytes()
        while self._readable:
            temp = self.read()
            result += temp
            index = result.find(self.HTTP_HEAD_BODY_SEP)
            if index != -1:
                self._read_buffer = result[index+4:]
                break
        else:
            raise Exception("http request data error ({},{})".format(result, self._readable))
        return result[0:index]

    def read_body_data(self, target = None):
        result = self._read_buffer
        self._read_buffer = bytes()
        if not self._readable:
            return result
        else:
            if target:
                target(result)
            while self._readable:
                temp = self.read()
                if target:
                    target(temp)
                else:
                    result += temp
            if not target:
                return result        

    def write(self, data):
        if data:
            self._write_buffer += data

    def flush(self):
        self._sock.sendall(self._write_buffer)
        self._write_buffer = bytes()

    def write_in_stream(self, stream):
        for data in iter(stream):
            self._sock.sendall(stream)

    def write_data_in_stream(self, data):
        size = self.DEFAULT_WRITE_SIZE
        def stream():
            length = len(data)
            index = 0
            while index < length:
                index += size
                yield data[index - size, index]
        self.write_in_stream(stream())