import os
import json
from pprint import pprint

def get_files_in_dirs(dirs):
    files = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        files += os.listdir(d)
    return files

def get_files_in_dirs_with_locations(dirs):
    files = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        files.append({
            'execs': os.listdir(d),
            'directory': d
        })
    return files

def get_files_in_path():
    env_path = os.environ['PATH']
    path_dirs = env_path.split(':')
    return get_files_in_dirs(path_dirs)


def print_files_in_path():
    files_in_path = get_files_in_path()
    print(json.dumps(files_in_path, indent=4))

# print_files_in_path()

if __name__ == "__main__":
    import sys
    files_in_path = get_files_in_path()
    if len(sys.argv) >= 2:
        print("PYTHON : PATH={}, files_in_path: {}, dumping to {}".format(os.environ['PATH'], len(files_in_path), sys.argv[1]))
        with open(sys.argv[1], 'w') as f:
            json.dump(files_in_path, f)
    else:
        pass
        #pprint(files_in_path)
