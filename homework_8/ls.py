#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser('List directory contents')
parser.add_argument('dir', nargs='?', default=os.getcwd(),
                    help='directory')
parser.add_argument('-a', action='store_true',
                    help='Include directory entries whose names begin with a dot')
args = parser.parse_args()

def starts_with_dot(name):
    
    if name[0] == '.':
        return False
    else:
        return True

try:
    allfiles = os.listdir(args.dir)
    if args.a:
        print('\n'.join(sorted(allfiles)))
    else:
        files = list(sorted(filter(starts_with_dot, allfiles)))
        print('\n'.join(files))
        
except FileNotFoundError:
    print("Directory doesn't exist")
except NotADirectoryError:
    print("It isn't directory")

