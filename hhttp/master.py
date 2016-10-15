import os, sys, socket, selectors
from manager import Manager
import consts

#the most efficient select implementation available on the current platform
SELECT = selectors.DefaultSelector()
CPU_NUM = os.cpu_count()

#ipv4
AF = socket.AF_INET #AF_INET6
HOST = '127.0.0.1'
PORT = 80

SOCK = socket.socket(AF, socket.SOCK_STREAM)
SOCK.bind((HOST, PORT))
SOCK.listen(100)
SOCK.setblocking(False)
SELECT.register(SOCK, selectors.EVENT_READ)

M = Manager(CPU_NUM)

while True:
    events = SELECT.select()
    for key, _ in events:
        if key.fileobj is SOCK:
            conn, addr = SOCK.accept()
            conn.setblocking(False)
            SELECT.register(conn, selectors.EVENT_READ)
        else:
            SELECT.unregister(key.fd)
            M.put(key.fileobj)