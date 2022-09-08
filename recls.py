"""Print the """

from ast import Store
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
parser.add_argument('-g', '--glob', type=str, default='*',
    help='Glob to match for')
args = parser.parse_args()




def partition(pred, seq):
    """Make so can pass list of *preds and filter with all?"""
    seq_copy1, seq_copy2 = tee(seq)
    return filter(pred, seq_copy1), filter(lambda v: not pred(v), seq_copy2)

partition_files_and_dirs =lambda i: partition(lambda p: p.is_dir(), i)


def recursive_ls(path, show_all, max_depth, current_depth=0):
    if current_depth > max_depth:
        return
        
    dirs, files = partition_files_and_dirs(path.iterdir())

    if not show_all:
        dirs = filter(lambda d: not d.name.startswith('.'), dirs)
        files = filter(lambda d: not d.name.startswith('.'), files)

    indent = "  " * current_depth

    for d in dirs:
        print(indent, '-', d.name, ':file_folder:', style='turquoise2')
        recursive_ls(d, show_all, max_depth, current_depth+1)

    for i, f in zip(range(5), files):
        print(indent, '-', f.name)
        if i == 4: 
            print(f'{indent} .\n{indent} .\n{indent} .')



if __name__ == '__main__':
    path = Path(args.path)
    recursive_ls(path, args.depth, args.all)
