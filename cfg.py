#!/usr/bin/python
import os

def parse(f):
    top = {}
    current = top
    stack = []
    last = None

    for line in f:
        line, _, _ = line.partition('//')
        line = line.strip()
        if not line: continue
        if '=' in line:
            k, _, v = line.partition('=')
            current[k.strip()] = v.strip()
            continue
        if line == '{':
            new = {}
            if isinstance(current.get(last), str): # same tag used as both foo=bar and foo{}
                del current[last]
            current.setdefault(last, []).append(new)
            stack.append(current)
            current = new
            continue
        if line == '}':
            current = stack.pop()
            last = None
            continue
        last = line
    return(top)

_config_cache = {}
def get_config(fn):
    if fn not in _config_cache:
        try:
            with open(fn, 'r') as f:
                _config_cache[fn] = parse(f)
        except IOError:
            return
    return _config_cache[fn]

def get_default_config():
    ksppath = os.environ.get('KSPPATH')
    if ksppath is None:
        return
    path = os.path.join(ksppath, 'GameData', 'ModuleManager.ConfigCache')
    return get_config(path)

def fetchall(node, key):
    res = []
    for c in node:
        res.extend(c.get(key, []))
    return res

if __name__ == '__main__':
    import sys, pprint
    pprint.pprint(get_default_config())
