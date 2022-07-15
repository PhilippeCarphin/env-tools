#!/usr/bin/env python3

import argparse
import os
from philenv import *
from envtool import get_command
from envdiff import diff_command
from env_find import find_in_env_command
from symbolboss import find_symbol_command

p = argparse.ArgumentParser(description="""
Analyze current computing environment and effect of
certain commands on the environemnt.  

(Run 'envtool SUBCOMMAND --help' for help on subcommands
 or 'envtool help SUBCOMMAND' for manual page on SUBCOMMAND) """)
sp = p.add_subparsers()

diff_parser = sp.add_parser('diff')
diff_parser.add_argument('--shell', choices=['bash', 'zsh', 'fish'], help="Output shell code for selected shell representing the environment change")
diff_parser.add_argument('--executables', action='store_true', help="Compare executables findable through PATH before and after command instead of comparing environements")
diff_parser.add_argument('posargs', nargs='*')
diff_parser.set_defaults(command=diff_command)

get_parser = sp.add_parser('get')
get_parser.add_argument('posargs', nargs='*')
get_parser.set_defaults(command=get_command)

find_parser = sp.add_parser('find', description="Find files in directories mentionned in environment variables")
find_parser.add_argument('needle', help="filename or regex")
find_parser.add_argument('--exact', action='store_true')
find_parser.set_defaults(command=find_in_env_command)

find_symbol_parser = sp.add_parser('find-symbol')
find_symbol_parser.add_argument('needle')
find_symbol_parser.add_argument('--exact', action='store_true')
find_symbol_parser.add_argument('--demangle', action='store_true')
find_symbol_parser.add_argument('--nice', action='store_true')
find_symbol_parser.set_defaults(command=find_symbol_command)

def phil_help_command(args):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ['MANPATH'] = os.path.normpath(os.path.join(this_dir, '..', '..', 'share', 'man'))
    os.execl('/usr/bin/env', '/usr/bin/env', 'man', f'{args.posarg[0]}')

help_parser = sp.add_parser('help', description="Show manpage for envtool-command")
help_parser.add_argument('posarg', nargs=1)
help_parser.set_defaults(command=phil_help_command)


def f():
    pass

function = type(f)

args = p.parse_args()
if not isinstance(args.command, function):
    raise Exception("--func parameter is for internal use only")

try:
    args.command(args)
except KeyboardInterrupt:
    pass

# print(f"sys.argv[0] = {sys.argv[0]}")
