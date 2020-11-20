import argparse
import envtool
from philenv import *


def diff_command(args):
    print(f'args.posargs : {args.posargs}')
    envs = envtool.env_diff(' '.join(args.posargs))
    if args.shell:
        envtool.get_effect(envs['before'], envs['after'])
    print(envtool.compare_envs(envs['before'], envs['after']))


p = argparse.ArgumentParser()
sp = p.add_subparsers()

diff_parser = sp.add_parser('diff')
diff_parser.add_argument('--shell', choices=['bash', 'zsh', 'fish'])
diff_parser.add_argument('--executables', action='store_true')
diff_parser.add_argument('posargs', nargs='*')
diff_parser.set_defaults(func=diff_command)

find_symbol_parser = sp.add_parser('find-symbol')
find_symbol_parser.set_defaults(func=lambda args : print(f'find-symbol : {args}'))


args = p.parse_args()

args.func(args)
