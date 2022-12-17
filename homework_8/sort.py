#!/usr/bin/env python

import argparse
import sys

parser = argparse.ArgumentParser('The sort utility sorts text and binary files by lines.')
parser.add_argument('file', default=None, nargs='?',
                    help='File for sorting')
args = parser.parse_args()

if args.file:
    text = open(args.file).readlines()
else:
    text = sys.stdin.readlines()

print(''.join(sorted(text)), end='')
