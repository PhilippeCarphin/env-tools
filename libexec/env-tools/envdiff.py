
from pathdiff import path_diff
import json
import textwrap
import envtool
import sys
import subprocess

def get_effect(env_before, env_after):
    ''' Outputs shell code representing the difference
    between the two environments.

    Ideally, 'envdiff --shell SHELL COMMAND' will produce
    code for SHELL exporting new variables, unsetting deleted
    variables and modifying new variables.
    '''
    new_vars = set(env_after.env) - set(env_before.env)
    deleted_vars = set(env_before.env) - set(env_after.env)
    common_vars = set(env_before.env).intersection(set(env_after.env))

    report = []
    report.append('# \033[1;32m========== New variables ===========\033[0m')
    for var in sorted(new_vars):
        report.append(env_after.get_declaration(var))

    report.append('# \033[1;31m========== Deleted variables =======\033[0m')
    for var in sorted(deleted_vars):
        report.append(env_before.get_unsetting(var))

    report.append('# \033[1;32m========= Changed Vars =============\033[0m')
    for var in sorted(common_vars):
        before = env_before.env[var]
        after = env_after.env[var]
        if before != after:
            report.append(env_before.get_change(var, before, after))
    return '\n'.join(report)


def compare_envs(env_before, env_after):
    ''' Return a string giving a report of the differences between the two
    environment objects '''
    new_vars = set(env_after.env) - set(env_before.env)
    deleted_vars = set(env_before.env) - set(env_after.env)
    common_vars = set(env_before.env).intersection(set(env_after.env))
    modified_vars = []
    unchanged_vars = []
    for var in sorted(common_vars):
        before = env_before.env[var]
        after = env_after.env[var]
        if before == after:
            unchanged_vars.append(var)
        else:
            modified_vars.append(var)

    report = []

    report.append('# \033[1;34m========== unchanged variables ===========\033[0m')
    for var in sorted(unchanged_vars):
        before = env_before.env[var]
        after = env_after.env[var]
        report.append(env_after.get_pretty_str(var))

    report.append('# \033[1;32m========== New variables ===========\033[0m')
    for var in sorted(new_vars):
        report.append(env_after.get_pretty_str(var))

    report.append('# \033[1;31m========== Deleted variables =======\033[0m')
    for var in sorted(deleted_vars):
        report.append(env_before.get_pretty_str(var))

    report.append('# \033[1;33m========= Changed Vars =============\033[0m')
    for var in sorted(modified_vars):
        before = env_before.env[var]
        after = env_after.env[var]
        if var in envtool.comparers:
            result = envtool.comparers[var](before, after)
            if result != '':
                report.append(var + '\n' + result)
        else:
            report.append(textwrap.dedent(f'''
                {var}
                    BEFORE: {env_before.get_str(var)}
                     AFTER: {env_after.get_str(var)}
                ''').strip()
            )

    return '\n'.join(report)


def env_diff(command):
    # We could get this envrionment by just doing
    # env_before = envtool.EnvWrapper.from_environment_dict()
    # but we do both the same way so that things like SHLVL will match up
    # in both
    before_script = f'''
    {sys.executable} -c 'import json, os ; print(json.dumps(dict(os.environ)))'
    '''
    result = subprocess.run(before_script, shell=True, universal_newlines=True, stdout=subprocess.PIPE, check=True)
    env_before = envtool.EnvWrapper.from_environment_dict(json.loads(result.stdout))

    after_script = f'''
    eval {command} 1>&2
    echo "Command {command} complete" >&2
    {sys.executable} -c 'import json, os ; print(json.dumps(dict(os.environ)))'
    # Redirect 1 to 2 in case the command has set up traps that may print to stdout
    exec 1>&2
    '''
    result = subprocess.run(after_script, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(f"{sys.argv[0]} : \033[33mWARNING\033[0m: command returned non-zero exit code {result.returncode}")

    if result.stdout.strip() == "":
        print(f'{sys.argv[0]}: \033[1;31mERROR\033[0m: Command failed, could not get environment after command')
        return None

    env_after = envtool.EnvWrapper.from_environment_dict(json.loads(result.stdout))

    return {
        'before': env_before,
        'after': env_after
    }


def diff_command(args):
    envs = env_diff(' '.join(args.posargs))
    if envs is None:
        return
    if args.shell:
        print(get_effect(envs['before'], envs['after']))
    elif args.executables:
        path_diff(envs['before']['PATH'], envs['after']['PATH'])
    else:
        print(compare_envs(envs['before'], envs['after']))
