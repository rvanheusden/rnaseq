#!/usr/bin/env python3

import argparse
from concurrent.futures import ThreadPoolExecutor
from subprocess import Popen, PIPE
import sys

def getlines(path):
    if path.startswith("<(") and path.endswith(")"):
        cmd = path[2:-1]

        with Popen(cmd, shell=True, stdout=PIPE) as process:
            return [line.decode('utf-8') for line in process.stdout.readlines()]

    with open(path) as file:
        return file.readlines()

def paste(delimiter, files):
    executor = ThreadPoolExecutor()
    file_lines = list(executor.map(getlines, files))
    num_lines = max((len(lines) for lines in file_lines))

    for n in range(num_lines):
        first = True
        for lines in file_lines:
            if first:
                first = False
            else:
                sys.stdout.write(delimiter)

            if len(lines) <= n:
                continue

            sys.stdout.write(lines[n].rstrip('\n'))

        sys.stdout.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""A partial paste command implementation in Python.""")
    parser.add_argument("-d", "--delimiter", dest="delimiter", default='\t', type=str)
    parser.add_argument("files", metavar="file", type=str, nargs='+')
    args = parser.parse_args()
    paste(args.delimiter, args.files)
