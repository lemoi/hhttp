import re

MIME_TYPES = dict()
with open('hhttp/mime.types') as fp:
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

HTTP_STATUS_CODE = dict()
with open('hhttp/http_status_code.types') as fp:
    for raw in fp:
        result = re.match('^\s*(\S+)\s+(\S.*?\S)\s*$', raw)
        if result:
            m = result.groups()
            fk = m[0]
            bk = m[1]
            HTTP_STATUS_CODE[fk] = bk

CONFIG_PARAM = dict()
with open('config.ini') as fp:
    for raw in fp:
        result = re.match('^\s*(\S+)\s*=\s*(\S.*?\S)\s*$', raw)
        if result:
            m = result.groups()
            fk = m[0]
            bk = m[1]
            CONFIG_PARAM[fk] = bk

SERVER_NAME = 'hhttp'    