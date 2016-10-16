import os
import multiprocessing
import socket
import random
import time
from .handler import *

class Worker():
    def __init__(self, q):
        print('{} ready'.format(multiprocessing.current_process()))
        self._tasks = q
        self._pid = os.getpid()
        self._handler = StaticFileHandler()
        self.run()

    def run(self):
        while True:
            sock = self._tasks.get()
            try: 
                print('process(pid = {})'.format(self._pid))
                self._handler.do_with(sock)
            except BrokenPipeError:
                pass
            except Exception as e:
                print("error", e)
            finally:
                print('')
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()