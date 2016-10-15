import os
import multiprocessing
import socket
import random
import time
import handler

class Worker():
    def __init__(self, q):
        print('{} ready'.format(multiprocessing.current_process()))
        self._tasks = q
        self._pid = os.getpid()
        self._handler = handler.StaticFileHandler()
        self.run()

    def run(self):
        while True:
            sock = self._tasks.get()
            try: 
                print('deal with', sock)
                self._handler.do_with(sock)
            except BrokenPipeError:
                pass
            except Exception as e:
                print("error", e)
            finally:
                print('')
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()