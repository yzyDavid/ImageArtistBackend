import hashlib
import os


def hash_filename(f) -> str:
    sha1 = hashlib.sha1()
    sha1.update(f.read())
    f.seek(0)
    return sha1.hexdigest() + os.path.splitext(f.filename)[1]
