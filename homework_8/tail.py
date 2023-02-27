#!/usr/bin/env python

import argparse
import sys

parser = argparse.ArgumentParser('display the last part of a file')
parser.add_argument('file', default=None, nargs='?',
                    help='File for reading')
parser.add_argument('-n', '--lines', default=0, type=int,
                    help='The location is number lines')
args = parser.parse_args()

if args.file:
    text = open(args.file).readlines()
else:
    text = sys.stdin.readlines()
    
lines_text = len(text)

try: 
    if args.lines >= lines_text:
        print(''.join(text), end='')
    else:
        print(''.join(text[-args.lines:]), end='')
            
except FileNotFoundError:
    print("File doesn't exist")
except IsADirectoryError:
    print("It's a directory")
