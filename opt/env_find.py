#!/usr/bin/python


import os
import re

def dir_contains(d,search_string):
    # print('dir_contains({}, {})'.format(d,search_string))
    try:
        contents = os.listdir(d)
    except OSError as e:
        print(e)
        return False
    for f in contents:
        if search_string in f:
            return True
    return False

def find_in_env(f, type='contains', custom_match=None):
    results = []
    for var in os.environ:
        results += find_in_value(var, os.environ[var], f, type, custom_match)
    return results

def find_in_value(var, value,search_string, type='endswith', custom_match=None):
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
    elif type == 'custom':
        match = custom_match
    else:
        raise TypeError("'type parameter has unhandled value {}".format(type))

    results = []
    if ':' in value:
        # print('yes colons in {}'.format(value))
        dirs = value.split(':')

        for d in dirs:
            if not os.path.isdir(d):
                continue
            try:
                contents = os.listdir(d)
            except OSError as e:
                print(e)
                continue

            for file in contents:
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

