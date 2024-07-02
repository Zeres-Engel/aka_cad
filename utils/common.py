import os
import shutil
import time

def create_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
    except:
        pass
    os.mkdir(folder_path)


def get_time():
    return str(time.time()).replace(".", "_")