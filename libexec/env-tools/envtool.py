#!/usr/bin/env python3

'''
This class takes the environment and represents it in a way that can be
specified by the user.  If no specification is given, the representation
will be equivalent to the os.environ dictionary.

The user
'''

import os
import sys
import json
import subprocess
import re
from pprint import pprint


def make_decorator(dictionary):
    '''
    Creates a decorator that adds the function to a dictionary under the keys
    listed in args

    '''
    class env_decorator:
        def __init__(self, args):
            self.args = args
        def __call__(self, f):
            for var in self.args:
                dictionary[var] = f
            return f
    return env_decorator

# Functions taking string values and returning string, lists or dictionaries
# Decorating a function with this decorator with argument list_of_vars
# will register that function as the parser for the values of the variables in
# the list list_of_vars
parsers = {}
parses = make_decorator(parsers)

# Functions taking variable name and value and returning string
stringizers= {}
stringizes = make_decorator(stringizers)

# Functions taking variable name and value and returning string
pretty_stringizers = {}
pretty_stringizes = make_decorator(pretty_stringizers)

''' Dictionnary of comparison functions '''
# Functions taking object before and object after and returning a string
comparers = {}
compares = make_decorator(comparers)

updaters = {}
updates = make_decorator(updaters)

def _get_stringizer(varname):
    for key, func in stringizers.items():
        if re.fullmatch(key, varname):
            return func
    return str

def _get_pretty_stringizer(varname):
    for key, func in pretty_stringizers.items():
        if re.fullmatch(key, varname):
            return func
    return str

def _get_comparer(varname):
    for key, func in comparers.items():
        if re.fullmatch(key, varname):
            return func
    return None


class EnvWrapper:
    ''' Class that encapsulates a dictionnary of environment variables
    The keys are variable names and the values are the parsed string values
    of the environment variables as defined by the 'processor' functions '''
    def __init__(self, d=None, representation=None):
        ''' Create an instance from an already made dictionary or from the
        environment dictionary from os.environ. '''
        if representation:
            self.env=representation
        elif d:
            self.env=self.decode_environment_dict(d)
        else:
            self.env = self.decode_environment_dict(os.environ)

    def __getitem__(self, key):
        return self.env[key]

    def __iter__(self):
        return iter(sorted(self.env))

    def __str__(self):
        return str(self.env)

    def get_str(self, key):
        '''Returns a string representing the environment variable. This string may or
        may not be equal to the string value of the variable using function
        registered as the 'stringizer' for that vaiable

        '''
        if key in self.env:
            stringizer = _get_stringizer(key)
            print(f"stringizer for '{key}' is {stringizer}")
            return f"{key}={stringizer(self.env[key])}"
        else:
            return key + ' is not in environment'

    def get_pretty_str(self, key):
        ''' Get a pretty representation of the variable '''
        if key in self.env:
            pretty_stringizer = _get_pretty_stringizer(key)
            print(f"pretty_stringizer for '{key}' is {pretty_stringizer}")
            return f"{key}={pretty_stringizer(self.env[key])}"
        else:
            return key + ' is not in environment'

    def json_dumps(self):
        ''' Dump the dictionary of variabl and their parsed values '''
        return json.dumps(self.env)

    def pretty(self):
        ''' Return a string formed by all the pretty printed variables '''
        return '\n'.join(self.get_pretty_str(key) for key in self)

    def to_file(self, filename):
        with open(filename, 'w') as f:
            json_dump(f, self.env, indent=4)

    @staticmethod
    def decode_environment_dict(d):
        ''' Transform the os.environ dictionary to the format that I use:
        Each variable can have a function that parsed the string value into a
        list or dictionary or what ever else you want. '''
        representation = {}
        for var, value in d.items():
            if var in parsers.keys():
                representation[var] = parsers[var](value)
            else:
                representation[var] = d[var]
        return representation

    @classmethod
    def from_environment_dict(cls, d=None):
        if not d:
            d = os.environ
        return cls(representation=cls.decode_environment_dict(d))

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            representation = json.load(f)
        return cls(representation=representation)

    def get_declaration(self, var):
        if var.endswith('%%'):
            # Env has 'BASH_FUNC_<name>%%=() {...\n}'
            func_name = var[len('BASH_FUNC_'):-len('%%')]
            func_value = self.env[var][len('() {'):]
            return f"{func_name}(){{\n{func_value}\nexport -f {func_name}"

        if var in stringizers:
            return f"{var}=stringizers[var](self.env[var])"

        return f"{var}=str(self.env[var])"

    def get_unsetting(self, var):
        if var.endswith('%%'):
            return f'unset -f {var[len("BASH_FUNC_"):-len("%%")]}'
        return f'unset {var}'

    def get_change(self, var, before, after):
        if isinstance(before, list):
            if after:
                new_elements = set(after) - set(before)
                return f"{var}=\"${var}:{':'.join(new_elements)}\""
            else:
                return f'{var}=""'
        elif var in stringizers:
            return f'{var}="{stringizers[var](after)}"'
        else:
            return f'{var}="{after}"'



'''
================================================================================
Definitions of the processing and string functions
For any variable, you can define a function that parses it (taking a string
to any type of object)
For any variable, you can define a function that will take a variable name and a
ivalue and return a string.
Same thing for the pretty_stringizes
================================================================================
'''
''' Dictionaries with accompanying decorators used to register the functions
that process variables from string values and puts them back as strings in a
pretty way or in a normal way'''


def get_command(args):
    env = EnvWrapper.from_environment_dict()
    if args.posargs:
        for var in args.posargs:
            print(env.get_pretty_str(var))
    else:
        print(env.pretty())
