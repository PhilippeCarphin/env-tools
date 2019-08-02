#!/usr/bin/python

import os

def dir_contains(d,search_string):
    # print('dir_contains({}, {})'.format(d,search_string))
    for f in os.listdir(d):
        if search_string in f:
            return True
    return False

def find_in_env(f):
    results = []
    for var in os.environ:
        results += find_in_value(var, os.environ[var], f)
    return results

def find_in_value(var, value,search_string):
    # print('find_in_value({}, {}, {})'.format(var, value, search_string))
    results = []
    if ':' in value:
        dirs = value.split(':')

        for d in dirs:
            if not os.path.isdir(d):
                continue

            for file in os.listdir(d):
                if search_string in file:
                    results.append({
                        'file': file,
                        'location': d,
                        'variable': var
                    })

    else:
        # print("no colons in {}".format(value))
        if os.path.isdir(var):
            for file in os.listdir(var):
                if file.startswith(search_string):
                    results.append({
                        'file': file,
                        'location': value,
                        'variable': var
                    })

    return results


if __name__ == '__main__':
    import sys
    from pprint import pprint
    needle = sys.argv[1]
    pprint(find_in_env(needle))

