from urllib import request
import threading

def req():
	try:
		res = request.urlopen('http://127.0.0.1')
	except:
		pass
	else:
		print(res.read(1024))


for i in range(20):
	t = threading.Thread(target = req)
	t.start()