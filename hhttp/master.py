import os, sys, socket, selectors
from .manager import Manager
from .consts import CONFIG_PARAM

#the most efficient select implementation available on the current platform
SELECT = selectors.DefaultSelector()
CPU_NUM = os.cpu_count()

#ipv4
AF = socket.AF_INET #AF_INET6
HOST = CONFIG_PARAM['host']
PORT = int(CONFIG_PARAM['port'])


def run():
    SOCK = socket.socket(AF, socket.SOCK_STREAM)
    SOCK.bind((HOST, PORT))
    SOCK.listen(100)
    SOCK.setblocking(False)
    SELECT.register(SOCK, selectors.EVENT_READ)
    M = Manager(CPU_NUM)
    print('hhttp is running')
    while True:
        events = SELECT.select()
        for key, _ in events:
            if key.fileobj is SOCK:
                conn, addr = SOCK.accept()
                # conn.setblocking(False) 多线程 Resource temporarily unavailable 错误
                SELECT.register(conn, selectors.EVENT_READ)
            else:
                SELECT.unregister(key.fd)
                M.put(key.fileobj)