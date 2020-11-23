#!/usr/bin/env python3

import argparse
import envtool
import sys
import os
from pprint import pprint
from philenv import *
from env_find import find_in_env_command
from symbolboss import find_symbol_command

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
    pprint(list(res['gone']))
    print('============== added ==================')
    pprint(list(res['new']))
    print("PATHDIFF : #new={}, #kept={}, #gone={}".format(len(res['new']), len(res['kept']), len(res['gone']) ), file=sys.stderr)





def diff_command(args):
    print(f'args.posargs : {args.posargs}')
    envs = envtool.env_diff(' '.join(args.posargs))
    if args.shell:
        print(envtool.get_effect(envs['before'], envs['after']))
    elif args.executables:
        path_diff(envs['before']['PATH'], envs['after']['PATH'])
    else:
        print(envtool.compare_envs(envs['before'], envs['after']))

def get_command(args):
    env = envtool.EnvWrapper.from_environment_dict()
    if args.posargs:
        for var in args.posargs:
            print(env.get_pretty_str(var))
    else:
        print(env.pretty())


p = argparse.ArgumentParser()
sp = p.add_subparsers()

diff_parser = sp.add_parser('diff')
diff_parser.add_argument('--shell', choices=['bash', 'zsh', 'fish'])
diff_parser.add_argument('--executables', action='store_true')
diff_parser.add_argument('posargs', nargs='*')
diff_parser.set_defaults(func=diff_command)

get_parser = sp.add_parser('get')
get_parser.add_argument('posargs', nargs='*')
get_parser.set_defaults(func=get_command)

find_parser = sp.add_parser('find', description="Find files in directories mentionned in environment variables")
find_parser.add_argument('needle', help="filename or regex")
find_parser.add_argument('--exact', action='store_true')
find_parser.set_defaults(func=find_in_env_command)

find_symbol_parser = sp.add_parser('find-symbol')
find_symbol_parser.add_argument('needle')
find_symbol_parser.add_argument('--exact', action='store_true')
find_symbol_parser.add_argument('--demangle', action='store_true')
find_symbol_parser.add_argument('--nice', action='store_true')
find_symbol_parser.set_defaults(func=find_symbol_command)

args = p.parse_args()

try:
    args.func(args)
except KeyboardInterrupt:
    pass

# print(f"sys.argv[0] = {sys.argv[0]}")
