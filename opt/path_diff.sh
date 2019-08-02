#!/usr/bin/env bash


# Remembering full path to python3 may be necessary if you are doing things like
# $ pathdiff export PATH=''
PYTHON3_EXEC=$(which python3)
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

path_files_before=/tmp/$(whoami)_path_before.txt
path_files_after=/tmp/$(whoami)_path_after.txt

$PYTHON3_EXEC "$this_dir"/path_files.py "$path_files_before"
# shellcheck disable=SC2068
eval $@
$PYTHON3_EXEC "$this_dir"/path_files.py "$path_files_after"

$PYTHON3_EXEC "$this_dir"/path_compare.py "$path_files_before" "$path_files_after"
