from pprint import pprint
import sys
import json

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

initial_files = json.loads(open(sys.argv[1]).read())
final_files = json.loads(open(sys.argv[2]).read())
#
# pprint(get_difference(initial_files, final_files))
res = get_difference(initial_files, final_files)
pprint(res)
print(f"#new={len(res['new'])}, #kept={len(res['kept'])}, #gone={len(res['gone'])}")
