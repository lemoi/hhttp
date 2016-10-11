from multiprocessing import Process, Queue
from worker import Worker

class Manager():

	def __init__(self, p_num):
		self.p_num = p_num
		self._t_lists = []
		self._p_lists = []
		for i in range(p_num):
			q = Queue()
			p = Process(target = Worker, args = (q, ))
			p.start()
			self._t_lists.append(q)
			self._p_lists.append(p)

	def put(self, sock):
		self._t_lists[self.choose()].put(sock)

	def choose(self):
		m_index = 0
		m_size = self._t_lists[0].qsize()
		for i in range(1, self.p_num):
			size = self._t_lists[i].qsize()
			if  size < m_size:
				m_size = size
				m_index = i
		return m_index

	def display(self):
		info = 'Worker(pid = {}) remain {}\n'
		temp = str()
		for i, p in enumerate(self._p_lists):
			temp += info.format(p.pid, self._t_lists[i].qsize())
		print(temp)