from itertools import tee
from functools import reduce
from collections.abc import Iterable
from typing import Any, Callable, Tuple

def apply(funcs: Iterable[Callable], arg: Any) -> Any:
    """Call functions in funcs from left to right on arg and return result"""
    return reduce(lambda acc, f: f(acc), funcs, arg)
        

def partition(pred, seq):
    seq_copy1, seq_copy2 = tee(seq)
    return filter(pred, seq_copy1), filter(lambda v: not pred(v), seq_copy2)

is_dir = lambda p: p.is_dir()
partition_files_and_dirs =lambda i: partition(is_dir, i)