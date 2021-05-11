#!/usr/bin/python3

import pprint
import env_find
import subprocess
import re
import json

lib_with_numbers_regex = re.compile(r'\.(so|dylib|a)(\.[0-9]+)*')

def is_some_kind_of_lib(_, filename):
    return (lib_with_numbers_regex.search(filename) is not None)

def find_symbol_in_file(symbol, file, demangle=False):
    try:
        symbol_lines = nm_output(file, demangle).splitlines()[2:]
    except subprocess.CalledProcessError:
        return
    for line in symbol_lines:
        symbol_datum = parse_nm_line(line)
        if symbol_datum and symbol in symbol_datum['symbol']:
            yield symbol_datum

def parse_nm_line(line):
    words = line.split()
    if len(words) == 2:
        return {
            'address': None,
            'type': words[0],
            'symbol': ' '.join(words[1:])
        }
    elif len(words) == 3:
        return {
            'address': words[0],
            'type': words[1],
            'symbol': ' '.join(words[2:])
        }
    else:
        return None


def nm_output(file, demangle=False):
    cmd = ['nm', '-D']
    if demangle:
        cmd.append('--demangle')
    result = subprocess.run([*cmd, file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout

def find_symbol_in_env(symbol, demangle=False):
    try:
        from progress.bar import Bar
    except:
        print("run 'python3 -m pip install --user progress'")
    all_libs = list(env_find.find_in_env(None, type='custom', custom_match=is_some_kind_of_lib))
    try:
        for match in Bar('Looking for symbols in libs', suffix='%(index)d/%(max)d ETA %(eta)d').iter(all_libs):
            file_path = match['location'] + '/' + match['file']
            matching_symbols = list(find_symbol_in_file(symbol, file_path, demangle))
            if not matching_symbols:
                continue
            yield {
                'matching_symbols': matching_symbols,
                'file': file_path,
                'variable': match['variable']
            }
    except KeyboardInterrupt:
        pass

def test_find_symbol_in_file():
    print(find_symbol_in_file("TargetAsmParser", "/Users/pcarphin/.local/lib/libLLVMAArch64AsmParser.a"))

def test_find_symbol_in_env():
    print(find_symbol_in_env("TargetAsmParser"))
    pass


def find_symbol_command(args):
    results = list(find_symbol_in_env(args.needle, demangle=args.demangle))
    if args.nice:
        jq = subprocess.Popen(['jq'], stdin=subprocess.PIPE, universal_newlines=True)
        json.dump(results, jq.stdin)
        jq.stdin.close()
        jq.wait()
    else:
        pprint.pprint(results)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pprint.pprint(find_symbol_in_env(sys.argv[1]))
