import json


def invert_dict(d1):
    d2 = {}
    for key, value_list in d1.items():
        for value in value_list:
            d2[value] = key
    return d2


with open('modules.json', 'r') as f:
    fcs = json.load(f)

modules = ['math', 'typing', 'functools', 'string', 'hashlib', 'random', 'heapq', 're', 'numpy', 'cmath', 'itertools',
           'pandas', 'pytest', 'scipy', 'matplotlib', 'sklearn', 'pyglet', 'OpenGL', 'decimal', 'datetime',
           'collections', 'fractions']

fcs = invert_dict(fcs)
# print(fcs)
