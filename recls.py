#!/usr/bin/env python3

from ast import Store
from csv import field_size_limit
import os
import argparse 
from pathlib import Path
from itertools import tee

from rich.console import Console
print = Console().print

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, nargs='?', default=os.getcwd(),
    help='Directory from which to search, default current')
parser.add_argument('-a', '--all', action='store_true',
    help='Include files beginning with .')
parser.add_argument('-d', '--depth', type=int, default=1,   #add mutual incompatible group for inf
    help='Depth to display nested files, default 2')
args = parser.parse_args()


def partition(pred, seq):
    seq_copy1, seq_copy2 = tee(seq)
    return filter(pred, seq_copy1), filter(lambda v: not pred(v), seq_copy2)


#Helper functions for recursive_ls
partition_files_and_dirs =lambda i: partition(lambda p: p.is_dir(), i)
filter_out_startswith_dot =  lambda path: filter(lambda d: not d.name.startswith('.'), path)


def recursive_ls(path, show_all, max_depth, current_depth=0):
    try:
        if current_depth > max_depth:
            return
    
        dirs, files = partition_files_and_dirs(path.iterdir())

        if not show_all:
            dirs = filter_out_startswith_dot(dirs)
            files = filter_out_startswith_dot(files)

        indent = "  " * current_depth

        for d in sorted(dirs):
            print(indent, '-', d.name, ':file_folder:', style='turquoise2')
            recursive_ls(d, show_all, max_depth, current_depth+1)

        show_files(files, indent)

    except PermissionError as e:
        print(e)


def show_files(files, indent):
    for i, f in (iter:= enumerate(sorted(files))):
            print(indent, '-', f.name)
            if i == 4 and (remaining := (sum(1 for _ in iter))):
                print(indent, '-', f'+{remaining} others', style='yellow')



if __name__ == '__main__':
    path = Path(args.path)
    recursive_ls(path, args.all, args.depth, 0)
