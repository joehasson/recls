from itertools import tee
from functools import reduce
from collections.abc import Iterable
from typing import Any, Callable, Iterable, Tuple

def apply(funcs: Iterable[Callable], arg: Any) -> Any:
    """Call functions in funcs from left to right on arg and return result"""
    return reduce(lambda acc, f: f(acc), funcs, arg)

def make_filter(pred: Callable[[Any], bool]) -> Callable[[Iterable], filter]:
    """Take predicate function and return a function which applies corresponding filter"""
    return lambda x: filter(pred, x)

def partition(pred: Callable[[Any], bool], seq: Iterable) -> Tuple[filter, filter]:
    """Take a function pred and a sequence seq, return two filter objects containing
    elements of seq, the first (resp. second) containing those elements of seq
    for which pred returns True (False)"""
    seq_copy1, seq_copy2 = tee(seq)
    return filter(pred, seq_copy1), filter(lambda v: not pred(v), seq_copy2)

is_dir = lambda p: p.is_dir()
partition_files_and_dirs =lambda i: partition(is_dir, i)

filter_out_files = make_filter(is_dir)
filter_hidden_files_and_dirs = make_filter(lambda path: not path.name.startswith('.'))
