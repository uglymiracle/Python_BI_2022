#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser('The cat utility reads files sequentially,writing them to the standard output.')
parser.add_argument('file', help='File for reading')
args = parser.parse_args()

try: 
    with open(args.file, 'r') as f:
        output = f.read()
        while len(output) > 0:
            print(output)
            output = f.read()
except FileNotFoundError:
    print("File doesn't exist")
except IsADirectoryError:
    print("It's a directory")
