import os, sys, socket, selectors

from manager import Manager

#the most efficient select implementation available on the current platform
SELECT = selectors.DefaultSelector
CPU_NUM = os.cpu_count()

#ipv4
AF = socket.AF_INET #AF_INET6
HOST = 
PORT = 

SOCK = socket.socket(AF, socket.SOCK_STREAM)
SOCK.bind((HOST, PORT))
SOCK.listen()
SOCK.setblocking(False)
SELECT.register(SOCK, selectors.EVENT_READ)

M = Manager(CPU_NUM)

while True:
	key, _ = SELECT.select()
	SELECT.unregister(key.fd)
	if key.fileobj is SOCK:
		conn, addr = SOCK.accept()
		SELECT.register(conn, selectors.EVENT_READ)
	else:
		M.put(key.fileobj)