#!/usr/bin/env python3

import os
import argparse 
from pathlib import Path
from typing import Tuple

from rich import print # type: ignore
from rich.tree import Tree # type: ignore

import recls_utils

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
    'all':  recls_utils.filter_hidden_files_and_dirs,
    'quiet': recls_utils.filter_out_files
} 


def build_tree(path: Path,
    filters: Tuple,
    t_depth: int,
    t: Tree=Tree('root', style='light_steel_blue')
    ) -> None:
    """Generates the rich Tree object which represents directory structure"""
    try:
        if t_depth:
            paths = recls_utils.apply(filters, path.iterdir())
            dirs, files = recls_utils.partition_files_and_dirs(paths)
            add_dir_branches(dirs, filters, t_depth-1, t)
            add_file_branches(files, t)
        return t
    except PermissionError as e:
        print(e)


def add_dir_branches(dirs: filter, filters: Tuple, branch_depth: int, t: Tree) -> None:
    """Add branches to tree t for each directory in path in-place"""
    for d in sorted(dirs):
        branch = t.add(f'[bold bright_cyan]{d.name}[/]' + " 📁")
        build_tree(d, filters, branch_depth, branch)


def add_file_branches(files, t) -> None:
    """Add branches to tree for each file in path in-place up to max of five"""
    for i, f in (iterator:= enumerate(sorted(files))):
        t.add(f.name, style='white')
        if i == 4 and (num_files_left := (sum(1 for _ in iterator))):
             t.add(f'+{num_files_left} others', style='yellow')


if __name__ == '__main__':
    path = Path(args.path)
    filters = tuple(v for k, v in arg_to_filters.items() if getattr(args, k))
    t = build_tree(path, filters, args.depth)
    print(t)
