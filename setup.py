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
        if line.find("import unittest, time, re") >= 0:
            lines.insert(count + 1, 'import os\n')
            lines.insert(count + 2, 'import sys\n')
            lines.insert(count + 3, "sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../')\n")
            lines.insert(count + 4, 'import utils\n')

        if line.find('self.base_url = "http://127.0.0.1:8000') >= 0:
            lines.insert(count + 3, '        utils.login(self.driver)\n')

        if line.find("self.driver.implicitly_wait(30)") >= 0:
			lines[count] = line.replace('30','10')

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
