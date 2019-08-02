#!/usr/bin/env python3

import os
import json
from pprint import pprint

exec_only = False

def get_files_in_dirs(dirs, exec_only=True):
    files = []
    for d in dirs:
        if not os.path.isdir(d):
            continue

        def is_executable(f):
            return os.access(os.path.join(d, f), os.X_OK) and not f.startswith('.nfs')

        if exec_only:
            files += list(
                filter(is_executable, os.listdir(d))
            )
        else:
            files += os.listdir(d)

    return files

def get_files_in_dirs_with_locations(dirs, exec_only=True):
    files = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        files.append({
            'execs': os.listdir(d),
            'directory': d
        })
    return files

def get_files_in_path(exec_only=True):
    env_path = os.environ['PATH']
    path_dirs = env_path.split(':')
    return get_files_in_dirs(path_dirs, exec_only=exec_only)


def print_files_in_path():
    files_in_path = get_files_in_path()
    print(json.dumps(files_in_path, indent=4))

# print_files_in_path()

if __name__ == "__main__":
    import sys
    files_in_path = get_files_in_path(exec_only)
    if len(sys.argv) >= 2:
        print("PYTHON : PATH={}, files_in_path: {}, dumping to {}".format(os.environ['PATH'], len(files_in_path), sys.argv[1]))
        with open(sys.argv[1], 'w') as path_file:
            json.dump(files_in_path, path_file)
    else:
        pass
        pprint(files_in_path)
