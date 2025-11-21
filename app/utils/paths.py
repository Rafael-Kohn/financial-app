import os

def root_path():
    return os.path.dirname(os.path.abspath(__file__ + "/.."))

def db_path(filename):
    return os.path.join(root_path(), filename)

def file_exists(path):
    return os.path.exists(path)
