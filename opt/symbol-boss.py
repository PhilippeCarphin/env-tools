#!/usr/bin/python

import env_find
import subprocess

def find_symbol_in_file(symbol, file):
    symbol_data = []

    try:
        symbol_lines = nm_output(file).split('\n')[2:]
    except subprocess.CalledProcessError:
        return []


    for line in symbol_lines:
        # print(line)
        words = line.split()
        symbol_datum = {}
        if len(words) == 2:
            symbol_datum = {
                'address': None,
                'type': words[0],
                'symbol': words[1]
            }
        elif len(words) == 3:
            symbol_datum = {
                'address': words[0],
                'type': words[1],
                'symbol': words[0]
            }
        else:
            # print("untreated nm output: ", words)
            continue

        if symbol in symbol_datum['symbol']:
            symbol_data.append(symbol_datum)
        else:
            pass #  print(f'symbol {symbol} not in {symbol_datum["symbol"]}')

    return symbol_data


def nm_output(file):
    # I was doing a pipe before which I wanted to pass
    # a single command string to BASH because I don't
    # know how to do pipes.

    # When I decided to do the searching in python instead
    # of piping through grep, I left this as is.  When I
    # went to put it back to just ["nm", file], it
    return subprocess.check_output([
        "bash", "-c", "nm " + file
    ]).decode('utf-8')

def find_symbol_in_env(symbol):

    static_libs = env_find.find_in_env('.a')
    shared_libs = env_find.find_in_env(None, 'so_with_numbers')

    results = []
    for match in static_libs:
        file_path = match['location'] + '/' + match['file']
        matching_symbols = find_symbol_in_file(symbol, file_path)
        if not matching_symbols:
            continue
        res = {
            'matching_symbols': matching_symbols,
            'file': file_path,
            'variable': match['variable']
        }
        results.append(res)
    return results

def test_find_symbol_in_file():
    print(find_symbol_in_file("TargetAsmParser", "/Users/pcarphin/.local/lib/libLLVMAArch64AsmParser.a"))

def test_find_symbol_in_env():
    print(find_symbol_in_env("TargetAsmParser"))
    pass

if __name__ == "__main__":
    import pprint
    import sys
    if len(sys.argv) > 1:
        pprint.pprint(find_symbol_in_env(sys.argv[1]))