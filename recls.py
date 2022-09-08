"""Print the """

import os
import argparse 
from pathlib import Path
from itertools import tee

from rich.console import Console
print = Console().print

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, nargs='?', default=os.getcwd(),
    help='Directory from which to search, default current')
parser.add_argument('-d', '--depth', type=int, default=1, 
    help='Depth to display nested files, default 2')
parser.add_argument('-g', '--glob', type=str, default='*',
    help='Glob to match for')
args = parser.parse_args()




def partition(pred, seq):
    """Make so can pass list of *preds and filter with all?"""
    seq_copy1, seq_copy2 = tee(seq)
    return filter(pred, seq_copy1), filter(lambda v: not pred(v), seq_copy2)

partition_files_and_dirs =lambda i: partition(lambda p: p.is_dir(), i)


def recursive_ls(path, max_depth, current_depth=0, indent = ""):
    if current_depth >= max_depth:
        return
        
    dirs, files = partition_files_and_dirs(path.iterdir())

    for d in filter(lambda v: not v.name.startswith('.'), dirs):
        print(indent, '-', d.name, ':file_folder:', style='turquoise2')
        recursive_ls(d, max_depth, current_depth+1, indent+"  ")

    for i, f in zip(range(5), files):
        if not f.name.startswith('.'):
            print(indent, '-', f.name)
        if i == 9: print(f'{indent} .\n{indent} .\n{indent} .')



if __name__ == '__main__':
    path = Path(args.path)
    recursive_ls(path, args.depth)
