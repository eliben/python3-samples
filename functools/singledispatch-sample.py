import collections
from functools import singledispatch

@singledispatch
def fun(arg, verbose=False):
    if verbose:
        print("Let me just say,", end=" ")
    print(arg)

@fun.register(collections.MutableMapping)
def _(arg, verbose=False):
    if verbose:
        print("The items in this mapping are:")
    for k, v in arg.items():
        print(k, '->', 'v')

fun('joe')
fun({2: 3, 4: 5})

