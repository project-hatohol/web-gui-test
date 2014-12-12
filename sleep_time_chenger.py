#! /usr/bin/env python

import os.path
import sys


def read_file(file_path):
    if os.path.exists(file_path):
        file = open(file_path)
        lines = file.readlines()
        file.close()
    
        return lines


def get_script_lines(file_path):
    lines = read_file(file_path)
    count = 0
    for line in lines:
        if line.find("time.sleep") >= 0:
            sec = line.split("(")[1].split(")")[0]
            lines[count] = line.replace(sec, sys.argv[2])

        count += 1

    return lines


def get_file_name(file_path):
    return file_path.split('/')[-1]


def make_script(file_path):
    lines = get_script_lines(file_path)
    name = get_file_name(file_path)
    f = open(name, "w")
    for line in lines:
        f.write(line)
    f.close()


if __name__ == '__main__':
    make_script(sys.argv[1])
