from urllib import request
import threading

def req():
    res = request.urlopen('http://www.baidu.com')
    rd = bytes()
    while True:
        temp = res.read(1024)
        if not temp:
            break
        rd += temp
    print(rd)

for i in range(1):
    t = threading.Thread(target = req)
    t.start()