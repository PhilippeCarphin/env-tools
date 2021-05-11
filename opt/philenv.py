#!/usr/bin/env python

import subprocess
import envtool
import json
''' This shows how you can specify what the tool does with various environment
variables.

I don't really like this idea anymore with the decorators.  Actually it is OK, but I'm actually not sure.

I want to create a wrapper tool for manipulating the environment.  So naturally
I came back to this code.  But now I think this code was only meant to look at
the environment and create reports.
'''


'''
================================================================================
SSH_CLIENT : We split based on spaces and using documentation, assign tokens to
their known meaning.
================================================================================
'''
@envtool.parses(['SSH_CLIENT'])
def process_ssh_client(value):
    tokens = value.split(' ')
    return {"ip":tokens[0],
            "port1": tokens[1],
            "port2":tokens[2],
            "rest":"_".join(tokens[3:])}

@envtool.stringizes(['SSH_CLIENT'])
@envtool.pretty_stringizes(['SSH_CLIENT'])
def pretty_str_ssh_client(value):
    print("PISS BUCKET")
    return ' '.join(value[k] for k in value).strip()


'''
================================================================================
colon list variables
================================================================================
Could this not just be replaced with
    elif var in colon_lists:
        ...

I'm actually having some trouble with this.  Any way, why would I even want to
look at
'''
colon_lists = [
    'CDPATH', 'PATH', 'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH',
    'CPATH', 'MIC_LD_LIBRARY_PATH', 'INFOPATH', 'OBJC_INCLUDE_PATH',
    'NLSPATH', 'LIBRARY_PATH', 'SSM_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH',
    'C_INCLUDE_PATH', 'MANPATH', 'EC_INCLUDE_PATH',
    'LIBPATH', 'PYTHONPATH', 'TCL_LIBRARY', 'LD_LIB_PATH', 'CRAY_LD_LIBRARY_PATH', 'LOADEDMODULES', '_LMFILES_',
]
space_lists = ['EC_LD_LIBRARY_PATH']
@envtool.parses(colon_lists)
def process_colon_list(value):
    if value == '':
        return []
    return list(sorted(value.strip(':').split(':')))
@envtool.parses(space_lists)
def process_space_list(value):
    return list(sorted(value.strip().split()))

@envtool.stringizes(colon_lists)
def colon_list_to_str(value):
    print(f'[colon_list_to_str]: value = {value}')
    return ':'.join(value)
@envtool.stringizes(space_lists)
def space_list_to_str(value):
    return ' '.join(value)


@envtool.pretty_stringizes(colon_lists)
def colon_list_to_pretty_str(value):
    return '    ' + '\n    '.join(value)

@envtool.compares(colon_lists + space_lists)
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

@envtool.updates(colon_lists)
def update_colon_list(before, after):
    if before:
        new = set(after) - set(before)
        gone = set(before) - set(after)
        kept = set(before).intersection(set(after))
        if new:
            return ':'.join(new)
        else:
            return None
    else:
        return ':'.join(after)


'''
================================================================================
SSH_CONNECTION
================================================================================
'''
ssh_connection = ['SSH_CONNECTION']
@envtool.parses(ssh_connection)
def process_space_list(value):
    return value.strip(' ').split(' ')

@envtool.stringizes(ssh_connection)
@envtool.pretty_stringizes(ssh_connection)
def space_list_to_str(value):
    return ' '.join(value)


'''
================================================================================
================================== MAIN PART ===================================
Take various actions based on command line arguments
================================================================================
'''
