from consts import HTTP_VERSION, HTTP_CRLF

class RequestHeaderParser:
    def __init__(self, data):
        chunk = data.decode('utf8').split(HTTP_CRLF)

        d = chunk[0].split(' ')
        self.method = d[0]
        pos = d[1].find("?")
        if pos != -1:
            self.req_path, self.query_string = d[1][0: pos], d[1][pos+1:]
        else:
            self.req_path = d[1]
            self.query_string = ''
            
        self.http_version = d[2]

        def parse_name_value(st):
            pos = st.index(':')
            name, value = st[0: pos], st[pos+1:]
            name = '-'.join(part.capitalize() for part in name.split('-'))
            return name.strip(), value.strip()

        self.headers = {}
        for header in chunk[1:]:
            name, value = parse_name_value(header)
            self.headers[name] = value

    def to_cgi_environ(self):
        environ = {
            "REQUEST_METHOD": self.method,
            "PATH_INFO": self.req_path,
            "QUERY_STRING": self.query_string,
            "CONTENT_TYPE": self.headers.get('Content-Type', ''),
            "CONTENT_LENGTH": self.headers.get('Content-Length', ''),
            "SERVER_PROTOCOL": self.http_version
        }
        return environ

class ResponseHeaderGenerator:
    def __init__(self, status_code):
        self.status_code = status_code
        self.headers = {}
        self.status_info = 'OK'

    def __setitem__(self, name, value):
        name = '-'.join(part.capitalize() for part in name.split('-'))
        self.headers[name] = value

    def to_bytes(self):
        status = HTTP_VERSION + ' ' + str(self.status_code) + ' ' + self.status_info
        res = [status]
        for name, value in self.headers.items():
            res.append(name + ': ' + value)
        return (HTTP_CRLF.join(res) + HTTP_CRLF * 2).encode('ascii')