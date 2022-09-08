"""Print the """

import os
import argparse 
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, nargs='?', default=os.getcwd(),
    help='Directory from which to search, default current')
parser.add_argument('-d', '--depth', type=int, default=2, 
    help='Depth to display nested files, default 2')
parser.add_argument('-g', '--glob', type=str, default='*',
    help='Glob to match for')
args = parser.parse_args()
from itertools import tee


def partition(pred, seq):
    seq_copy1, seq_copy2 = tee(seq)
    return filter(pred, seq_copy1), filter(lambda v: not pred(v), seq_copy2)


def recursive_ls(path, max_depth, current_depth=0, indent = ""):
    if current_depth >= max_depth:
        print(indent, '...')
        return
        
    dirs, files = partition(lambda p: p.is_dir(), path.iterdir())
    for d in dirs:
        if not d.name.startswith('.'):
            print(indent, d.name)
            recursive_ls(d, max_depth, current_depth+1, indent+"  ")
    for f in files:
        if not f.name.startswith('.'):
            print(indent, f.name)



if __name__ == '__main__':
    path = Path(args.path)
    recursive_ls(path, args.depth)
