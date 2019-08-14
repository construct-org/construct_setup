#!/bin/bash

THIS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PATH="$THIS/current/bin:$THIS/current/python/bin:$PATH"
export PYTHONPATH="$THIS/current/lib:$PYTHONPATH"

py_entry_point="$THIS/current/bin/construct"
source $py_entry_point

alias cons=construct


cons_set_version () {
    # Set active construct version
    rm "$THIS/current"
    ln -s "$THIS/$1" "$THIS/current"
}
