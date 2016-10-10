import os
import time

class Worker():
	def __init__(self, q):
		time.sleep(2)
		print('Worker : %d' % os.getpid())