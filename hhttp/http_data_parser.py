class RequestParser:
    def __init__(self, data):
        chunk = data.split(b'\r\n')
        self.req_body = chunk[-1] if chunk[-1] else None 

        ct = lambda b: b.decode('utf8')
        d = ct(chunk[0]).split(' ')
        self.method = d[0]
        self.req_path = d[1]
        self.http_version = d[2]

        def parse_name_value(chunk):
            st = ct(chunk)
            pos = st.index(':')
            name, value = st[0: pos], st[pos+1:] 
            return name.strip(), value.strip()

        self.headers = []
        for header in chunk[1: -2]:
            self.headers.append(parse_name_value(header))