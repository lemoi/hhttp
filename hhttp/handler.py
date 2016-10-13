from abc import ABC, abstractmethod
import multiprocessing

class Handler_Base(ABC):
    def __init__(self, q: multiprocessing.Queue):
        self._q = q

    def run(self):
        while True:
            sock = self._q.get()
            rd = bytes()
            try:
                while True:
                    temp = scck.recv(1024)
                    if not temp:
                        break
                    rd += temp
            except Exception as e:
                pass
            else:
                try:
                    sock.sendall(self.handle(rd))
                except Exception as e:
                    print('error :', e)
            finally:
                sock.shutdown(socket.SHUT_RDWR) #多进程环境下可能还存在对sock的引用，sock不会自动关闭，调用shutdown()关闭连接
                sock.close()

    @abstractmethod   
    def handle(self, input: bytes):
        """Handle input and return output"""
    