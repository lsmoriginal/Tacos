import hashlib

def shash(anything, length:int = None):
    """
    quick and stupid way of hashing anything into len=length
    """
    anything = str(anything)
    anything = anything.encode()
    anything = hashlib.md5(anything).hexdigest()
    anything = anything[:length]
    return anything
