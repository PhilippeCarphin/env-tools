#!/usr/bin/env bash

is_relative_link(){
    [[ $1 != /* ]]
}

follow_links()
{
    local file="$1"
    local curr_dir

    while [ -L $file ] ; do
        curr_dir="$(dirname $file)"
        file="$(readlink $file)"
        if is_relative_link $file ; then
            file="$curr_dir/$file"
        fi
        ls -l $file 1>&2
    done

    echo $file
}

this_dir=$(dirname $(follow_links ${BASH_SOURCE[0]}))

${this_dir}/envdiff source ssmuse-sh -d $1
