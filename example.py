import pyenv
import json

'''
================================================================================
SSH_CLIENT
================================================================================
'''
@pyenv.parses(['SSH_CLIENT'])
def process_ssh_client(value):
    tokens = value.split(' ')
    return {"ip":tokens[0],
            "port1": tokens[1],
            "port2":tokens[2],
            "rest":"_".join(tokens[3:])}

@pyenv.stringizes(['SSH_CLIENT'])
@pyenv.pretty_stringizes(['SSH_CLIENT'])
def pretty_str_ssh_client(var, value):
    return var + '=' + ' '.join(value[k] for k in value)


'''
================================================================================
colon list variables
================================================================================
'''
colon_lists = ['CDPATH', 'PATH', 'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH']
@pyenv.parses(colon_lists)
def process_colon_list(value):
    return value.strip(':').split(':')

@pyenv.stringizes(colon_lists)
def colon_list_to_str(var, value):
    return var + '=' + ':'.join(value)

@pyenv.pretty_stringizes(colon_lists)
def colon_list_to_pretty_str(var, value):
    prefix = var + '='
    joiner = '\n' + ' '*len(prefix)
    return prefix + joiner.join(value)

@pyenv.compares(colon_lists)
def compare_lists(before, after):
    new = set(after) - set(before)
    gone = set(before) - set(after)
    kept = set(before).intersection(set(after))
    indent = '\n      '
    result = ''
    if new:
        result += '    ADDED:' + indent + indent.join(new) + '\n'
    if (new or gone) and kept:
        result += '    KEPT:' + indent + indent.join(kept) + '\n'
    if gone:
        result += '    DELETED:' + indent + indent.join(gone) + '\n'
    return result.strip('\n')

'''
================================================================================
colon list variables
================================================================================
'''
space_lists = ['SSH_CONNECTION']
@pyenv.parses(space_lists)
def process_space_list(value):
    return value.strip(' ').split(' ')

@pyenv.stringizes(space_lists)
@pyenv.pretty_stringizes(space_lists)
def space_list_to_str(var, value):
    return var + '=' + ' '.join(value)


'''
================================================================================
================================== MAIN PART ===================================

Take various actions based on command line arguments
================================================================================
'''

if __name__ == "__main__":
    penv = pyenv.PyEnv()
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "dump":
            if len(sys.argv) > 2:
                with open(sys.argv[2], 'w') as f:
                    f.write(penv.json_dumps())
            else:
                print(penv.json_dumps())
        elif command == "pretty":
            print(penv.pretty())
        elif command == "get":
            print(penv.get_pretty_str(sys.argv[2]))
        elif command == 'compare':
            with open(sys.argv[2], 'r') as f:
                env_before = pyenv.PyEnv(json.loads(f.read()))
            with open(sys.argv[3], 'r') as f:
                env_after = pyenv.PyEnv(json.loads(f.read()))
            print(pyenv.compare_envs(env_before, env_after))
    else:
        print(penv.pretty())
