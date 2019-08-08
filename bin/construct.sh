#!/bin/bash

THIS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PATH="$THIS/latest/bin:$THIS/latest/python/bin:$PATH"
export PYTHONPATH="$THIS/latest/lib:$PYTHONPATH"

py_entry_point="$THIS/latest/bin/construct"
source $py_entry_point

alias cons=construct


cons_set_version () {
    # Set active construct version
    rm "$THIS/latest"
    ln -s "$THIS/$1" "$THIS/latest"
}
