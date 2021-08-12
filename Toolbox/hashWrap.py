import hashlib

def shash(anything, leng = None):

    anything = str(anything)
    anything = anything.encode()
    anything = hashlib.md5(anything).hexdigest()
    anything = anything[:leng]
    return anything