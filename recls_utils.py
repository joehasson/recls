from functools import reduce
from typing import Any, Callable, List, Tuple

def apply(funcs: List[Callable], *args: Any) -> Tuple[Any]:
    """Call functions in funcs from left to right on each input arg and return tuple of results"""
    return tuple(reduce(lambda acc, f: f(acc), funcs, initializer=arg) for arg in args)
        