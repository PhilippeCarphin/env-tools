#!/usr/bin/env python3

import os
from os import path

class SsmDomainError(BaseException):
    pass


def is_ssm_domain(d):

    if not os.path.isdir(d):
        return False

    if not 'etc' in os.listdir(d):
        return False

    if not 'ssm.d' in os.listdir(os.path.join(d,'etc')):
        return False

    return True


def excluded(d):
    if d.startswith('.'):
        return True

    return False

def has_match(string, file_list):
    for f in file_list:
        if string in f:
            return f
    return None

def find_ssm_domains(starting_point, depth=0):
    if is_ssm_domain(starting_point):
        # print("I am an ssm domain {}".format(starting_point))
        if needle in starting_point:
            #print("DOMAIN FOUND: {}".format(starting_point))
            domain = starting_point
            for arch in filter(lambda d: d in architecture_names, os.listdir(domain)):
                #print("         DOING ARCH {}".format(arch))
                d = os.path.join(domain, arch, 'bin')
                if os.path.isdir(d):
                    match = has_match(exec_to_find, os.listdir(d))
                    if match:
                        print("DOMAIN CONTAINING EXEC {} FOUND: {} (arch {})".format(match, domain, arch))
                d = os.path.join(domain, arch, 'lib')
                if os.path.isdir(d):
                    match = has_match(exec_to_find, os.listdir(d))
                    if match:
                        print("DOMAIN CONTAINING LIB  {} FOUND: {} (arch {})".format(match, domain, arch))
                d = os.path.join(domain, arch, 'lib', 'Linux_x86-64')
                if os.path.isdir(d):
                    match = has_match(exec_to_find, os.listdir(d))
                    if match:
                        print("DOMAIN CONTAINING LIB  {} FOUND: {} (arch {})".format(match, domain, arch))
                d = os.path.join(d, 'intel-2016.1.156')
                if os.path.isdir(d):
                    match = has_match(exec_to_find, os.listdir(d))
                    if match:
                        print("DOMAIN CONTAINING LIB  {} FOUND: {} (arch {})".format(match, domain, arch))
    else:
        for d in os.listdir(starting_point):
            subdir = os.path.join(starting_point, d)
            if d in ['.snapshot', 'etc', 'share', 'repo', 'PRIVATE', '__old'] or d.startswith('.'):
                # print("Not recursing into excluded directory {}".format(subdir))
                continue
            if os.path.isdir(subdir):
                # print("recursing into subdir: {}".format(subdir))
                try:
                    find_ssm_domains(subdir, depth+1)
                except PermissionError:
                    pass


os.path.isdir('/fs/ssm/eccc/cmd/cmda/log')

starting_point = '/fs/ssm/eccc/mrd/'


architecture_names = [
    'ubuntu-18.04-amd64-64',
    'all',
    'ubuntu-14.04-amd64-64',
    'sles-11-haswell-64-xc40',
]
dom = '/fs/ssm/eccc/mrd/rpn/rload/3.6'

def analyze_ssm_domain(dom, more=False):
    if not is_ssm_domain(dom):
        raise SsmDomainError("Directory {} is not an ssm domain".format(dom))

    architectures = {}
    for arch in os.listdir(dom):
        if arch in ['etc', 'lib']:
            continue
        if not more:
            if arch not in architecture_names and not more:
                print("UNKNOWN ARCHITECTURE : {}".format(arch))
                continue

        print("Doing arch {} of domain {}".format(arch, dom))
        arch_dir = os.path.join(dom, arch)
        arch_bin = os.path.join(arch_dir, 'bin')
        arch_lib = os.path.join(arch_dir, 'lib')
        architectures[arch] = {
            'execs': os.listdir(arch_bin),
            'libs': os.listdir(arch_lib) if os.path.isdir(arch_lib) else None
        }

    return {
        'domain': dom,
        'architectures': architectures
    }


# from pprint import pprint
# pprint(analyze_ssm_domain(dom))

# find_ssm_domains(dom)
needle = ''
exec_to_find = 'grib2_decode'
import sys
exec_to_find = sys.argv[1]
starting_point = sys.argv[2]
find_ssm_domains(starting_point)
