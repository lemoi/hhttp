import sys
def log(*args):
    sys.stdout.write(' '.join(args))
    sys.stdout.flush()