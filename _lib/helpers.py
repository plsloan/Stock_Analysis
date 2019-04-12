import os
import glob
import pandas
import datetime


def find_file(starting_path, filename):
    file_list = []
    for root, dirs, files in os.walk(starting_path):
        if filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list
def get_directories(path):
    list_dir = os.listdir(path)
    temp_dir = []
    for directory in list_dir:
        if '.' in directory:
            temp_dir.append(directory)
    for directory in temp_dir:
        list_dir.remove(directory)
    return list_dir
