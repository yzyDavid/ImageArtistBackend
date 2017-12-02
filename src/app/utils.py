import hashlib
import os
import functools
import time


def hash_filename(f) -> str:
    sha1 = hashlib.sha1()
    sha1.update(f.read())
    f.seek(0)
    return sha1.hexdigest() + os.path.splitext(f.filename)[1]


def perf_counter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        res = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f'perf_counter: {t2 - t1}')
        return res
    return wrapper
