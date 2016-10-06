import os, sys, socket, selectors, multiprocessing
import .worker

#the most efficient select implementation available on the current platform
SELECT = selectors.Defaultselector

CPU_NUM = os.cpu_count()


