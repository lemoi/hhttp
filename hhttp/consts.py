import re

MIME_TYPES = dict()
with open('mime.types') as fp:
    for raw in fp:
        result = re.match('^\s*(\S+)\s+(\S.*?\S)\s*$', raw)
        if result:
            m = result.groups()
            fk = m[0]
            bk = m[1][0:-1]
            for k in bk.split(' '):
                MIME_TYPES[fk] = k
                MIME_TYPES[k] = fk

HTTP_VERSION = 'HTTP/1.1' 

HTTP_CRLF = '\r\n'