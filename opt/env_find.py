#!/usr/bin/python


import os
import re

def dir_contains(d,search_string):
    # print('dir_contains({}, {})'.format(d,search_string))
    for f in os.listdir(d):
        if search_string in f:
            return True
    return False

def find_in_env(f, type='contains'):
    results = []
    for var in os.environ:
        results += find_in_value(var, os.environ[var], f, type)
    return results

def find_in_value(var, value,search_string, type='endswith'):
    # print('find_in_value({}, {}, {})'.format(var, value, search_string))
    if type == 'contains':
        def match(needle, heystack):
            return needle in heystack
    elif type == 'endswith':
        def match(needle, heystack):
            return heystack.endswith(needle)
    elif type == 'so_with_numbers':
        def match(needle, heystack):
            so_regex = re.compile(r'\.so(.[0-9]+)*')
            res = so_regex.search(heystack)
            return res is not None
    else:
        pass

    results = []
    if ':' in value:
        # print(f'yes colons in {value}')
        dirs = value.split(':')

        for d in dirs:
            if not os.path.isdir(d):
                continue

            for file in os.listdir(d):
                if match(search_string, file):
                    results.append({
                        'file': file,
                        'location': d,
                        'variable': var
                    })

    else:
        # print("no colons in {}".format(value))
        if os.path.isdir(var):
            for file in os.listdir(var):
                if match(search_string, file):
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

