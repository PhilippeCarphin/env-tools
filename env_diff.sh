#!/usr/bin/env bash

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

"$this_dir"/pyenv.sh dump > "$env_before_file"
# shellcheck disable=SC2068
eval $@
"$this_dir"/pyenv.sh dump > "$env_after_file"

"$this_dir"/pyenv.sh compare "$env_before_file" "$env_after_file"
