import os
from argparse import ArgumentTypeError

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise ArgumentTypeError(f"{path} is not a valid path")

def not_existing_dir_path(path):
    if os.path.isdir(os.path.dirname(path)):
        return path
    else:
        raise ArgumentTypeError(f"{path} is not a valid path")

def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise ArgumentTypeError(f"{path} is not a valid path")

def not_existing_file_path(path):
    if os.path.dirname(path) == "":
        path = os.path.join("./", path)
    return not_existing_dir_path(path)