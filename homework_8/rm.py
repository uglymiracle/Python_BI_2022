#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser('The rm utility attempts to remove the non-directory type files specified on the command line.')
parser.add_argument('path', nargs='+', 
                    help='path to file or directory')
parser.add_argument('-r', action='store_true',
                    help='Attempt to remove the file hierarchy rooted in each file argument.')
args = parser.parse_args()

if args.r:
    try:
        for path in args.path:
            for syst, dirs, files in os.walk(path, topdown=False):

                for name in files:
                    os.remove(os.path.join(syst, name))
                for name in dirs:
                    os.rmdir(os.path.join(syst, name))

            os.rmdir(path)
        
    except FileNotFoundError:
        print("File or directory doesn't exist")

else:
    try:
        for path in args.path:
            os.remove(path)
    except FileNotFoundError:
        print("File doesn't exist")
    except PermissionError:
        print("It's a directory")
