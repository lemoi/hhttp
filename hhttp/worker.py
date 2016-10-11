import os
import multiprocessing
import socket
import random
import time

class Worker():
	def __init__(self, q):
		print('{} ready'.format(multiprocessing.current_process()))
		self._tasks = q
		self._pid = os.getpid()
		self.handle()

	def handle(self):
		header = "HTTP/1.0 200 OK\r\nContent-type: text/plain; charset=utf-8\r\n\r\n"
		body = "Hello World(worker {} handle)".format(self._pid)
		res = (header + body).encode('ascii')
		while True:
			sock = self._tasks.get()
			rd = sock.recv(1024)
			# print('{} : {}'.format(self._pid, rd.decode('utf-8').split('\r\n')[-1]))
			time.sleep(random.randint(1, 2))
			try:
				sock.sendall(res)
			except Exception as e:
				print('error :', e)
			sock.shutdown(socket.SHUT_RDWR) #多进程环境下可能还存在对sock的引用，sock不会自动关闭，调用shutdown()关闭连接
			sock.close()