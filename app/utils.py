import os

def project(*args):
    return os.path.join(os.path.dirname(__file__), *args)