#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser('The mkdir utility creates the directories')
parser.add_argument('dir', help='directory')
parser.add_argument('-p', action='store_true',
                    help='Create intermediate directories as required.')
args = parser.parse_args()

if args.p:
    os.makedirs(args.dir)
else:
    try:
        os.mkdir(args.dir)
        
    except FileNotFoundError:
        print("Wrong path")
