#!/usr/bin/env python3

import os
import argparse 
from pathlib import Path

from rich import print
from rich.tree import Tree

from recls_utils import apply, is_dir, make_filter, partition_files_and_dirs


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, nargs='?', default=os.getcwd(),
    help='Directory from which to search, default current')
parser.add_argument('-a', '--all', action='store_false',
    help='Include files beginning with .')
parser.add_argument('-q', '--quiet', action='store_true',
    help='Do not include files, only directories')
parser.add_argument('-d', '--depth', type=int, default=2,
    help='Depth to display nested files, default 2')
args = parser.parse_args()


arg_to_filters = {
    'all':  make_filter(lambda path: not path.name.startswith('.')),
    'quiet': make_filter(is_dir)
} 


def build_tree(path, filters, t_depth, t= Tree('root', style='light_steel_blue')):
    """Generates the rich Tree object which represents directory structure"""
    try:
        if t_depth:
            paths = apply(filters, path.iterdir())
            dirs, files = partition_files_and_dirs(paths)
            add_dir_branches(dirs, filters, t_depth-1, t)
            add_file_branches(files, t)
        return t
    except PermissionError as e:
        print(e)


def add_dir_branches(dirs, filters, branch_depth, t) -> None:
    """Add branches to tree for each directory in path in-place"""
    for d in sorted(dirs):
        branch = t.add(f'[bold bright_cyan]{d.name}[/]' + " 📁")
        build_tree(d, filters, branch_depth, branch)


def add_file_branches(files, t):
    for i, f in (iterator:= enumerate(sorted(files))):
        t.add(f.name, style='white')
        if i == 4 and (num_left := (sum(1 for _ in iterator))):
             t.add(f'+{num_left} others', style='yellow')


if __name__ == '__main__':
    path = Path(args.path)
    filters = tuple(v for k, v in arg_to_filters.items() if getattr(args, k))
    t = build_tree(path, filters, args.depth)
    print(t)
