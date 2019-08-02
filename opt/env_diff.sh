#!/usr/bin/env bash

PYTHON_EXEC=$(which python)

is_relative_link(){
    [[ $1 != /* ]]
}

follow_links()
{
    local file="$1"
    local curr_dir

    while [ -L "$file" ] ; do
        curr_dir="$(dirname "$file")"
        file="$(readlink "$file")"
        if is_relative_link "$file" ; then
            file="$curr_dir/$file"
        fi
        ls -l "$file" 1>&2
    done

    echo "$file"
}


this_dir=$(dirname "$(follow_links "${BASH_SOURCE[0]}")")

env_before_file=/tmp/$(whoami)_env_before.txt
env_after_file=/tmp/$(whoami)_env_after.txt

"$PYTHON_EXEC" "$this_dir"/philenv.py dump > "$env_before_file"
# shellcheck disable=SC2068
eval $@
"$PYTHON_EXEC" "$this_dir"/philenv.py dump > "$env_after_file"

"$PYTHON_EXEC" "$this_dir"/philenv.py compare "$env_before_file" "$env_after_file"
