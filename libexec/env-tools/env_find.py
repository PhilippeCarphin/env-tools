#!/usr/bin/python

import os
import re
import sys
from pprint import pprint

def dir_contains(d,search_string):
    # print('dir_contains({}, {})'.format(d,search_string))
    try:
        contents = os.listdir(d)
    except OSError as e:
        print(e, file=sys.stderr)
        return False
    for f in contents:
        if search_string in f:
            return True
    return False

def find_in_env(f, type='contains', custom_match=None):
    for a in find_in_env_gen(f, type, custom_match):
        print(a, file=sys.stderr)
        yield(a)

def find_in_env_gen(search_string, type='contains', custom_match=None):
    for var in sorted(os.environ):
        yield from find_in_value(var, os.environ[var], search_string, type, custom_match)

def get_matches_from_dir(var, d, matcher, search_string):
    if '/' in search_string:
        words = search_string.split('/')
        d = os.path.join(d, *words[:-1])
        search_string = words[-1]
    print(f"\033[32mSearching in directory {d} from variable {var}\033[0m", file=sys.stderr)
    if not os.path.isdir(d):
        return
    for file in os.listdir(d):
        if matcher(search_string, file):
            yield {
                'file': file,
                'location': d,
                'variable': var
            }
so_regex = re.compile(r'\.so(.[0-9]+)*')
matcher_map = {
    'contains': lambda n,h: n in h,
    'exact': lambda n,h: n == h,
    'endswith': lambda n,h: h.endswith(n),
    'so_with_numbers': lambda n,h: so_regex.search(h) is not None
}

def find_in_value(var, value, search_string, type='endswith', custom_match=None):
    print(f"\033[1;35mSearching in directories from variable {var}\033[0m", file=sys.stderr)
    match = custom_match if custom_match else matcher_map[type]
    if os.path.isdir(value):
        yield from get_matches_from_dir(var, value, match, search_string)
    else:
        if ':' in value:
            dirs = value.split(':')
        elif ' ' in value:
            dirs = value.split(' ')
        else:
            dirs = []
        for d in filter(lambda d: os.path.isdir(d), dirs):
            yield from get_matches_from_dir(var, d, match, search_string)

def find_in_env_command(args):
    needle = args.needle
    match_type = 'contains'
    if args.exact:
        match_type = 'exact'
    pprint(list(find_in_env(needle, type=match_type)))

if __name__ == '__main__':
    import sys
    from pprint import pprint
    needle = sys.argv[1]
    pprint(find_in_env(needle))

