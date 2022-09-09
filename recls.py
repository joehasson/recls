#!/usr/bin/env python3

import os
import argparse 
from itertools import tee
from pathlib import Path

from rich import print
from rich.tree import Tree

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


def build_tree(path, show_all, max_depth, current_depth=0, t= Tree('')):
    try:
        if current_depth <= max_depth:
            dirs, files = partition_files_and_dirs(path.iterdir())

            if not show_all:
                dirs = filter_out_startswith_dot(dirs)
                files = filter_out_startswith_dot(files)

            for d in sorted(dirs):
                branch = t.add(f'[bold bright_cyan]{d.name}[/]' + " 📁")
                build_tree(d, show_all, max_depth, current_depth+1, branch)

            add_file_branches(t, files)
        return t

    except PermissionError as e:
        print(e)


def add_file_branches(t, files):
    for i, f in (iter:= enumerate(sorted(files))):
        t.add(f.name, style='white')
        if i == 4 and (num_left := (sum(1 for _ in iter))):
             t.add(f'+{num_left} others', style='yellow')



if __name__ == '__main__':
    path = Path(args.path)
    t = build_tree(path, args.all, args.depth)
    print(t)
