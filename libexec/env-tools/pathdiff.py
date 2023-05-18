import envtool
import os
import sys
from pprint import pprint

def get_execs_from_path(path):
    is_executable = lambda f: os.access(os.path.join(d, f), os.X_OK) and not f.startswith('.nfs')
    for d in path:
        if os.path.isdir(d):
            yield from filter(is_executable, os.listdir(d))
def get_difference(initial, final):
    s_final = set(final)
    s_initial = set(initial)
    new = s_final - s_initial
    gone = s_initial - s_final
    kept = s_final.intersection(s_initial)
    return {
        'new': new,
        'gone': gone,
        'kept': kept
    }
def path_diff(path_before, path_after):
    files_before = get_execs_from_path(path_before)
    files_after = get_execs_from_path(path_after)
    res = get_difference(files_before, files_after)
    print('============== removed ==================')
    pprint(list(sorted(res['gone'])))
    print('============== added ==================')
    pprint(list(sorted(res['new'])))
    print("PATHDIFF : #new={}, #kept={}, #gone={}".format(len(res['new']), len(res['kept']), len(res['gone']) ), file=sys.stderr)




