#!/bin/bash

construct () {
    # Shim around construct.sh installed in a virtualenv

    THIS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    OLD_PATH="$PATH"
    OLD_PYTHONPATH="$PYTHONPATH"
    export PATH="$THIS/latest/bin:$THIS/latest/python/bin:$PATH"
    export PYTHONPATH="$THIS/latest/lib:$PYTHONPATH"

    py_entry_point="$THIS/latest/bin/pyconstruct"
    $py_entry_point "$@"

    export PATH=$OLD_PATH
    export PYTHONPATH=$OLD_PYTHONPATH
}


cons () {
    # Alias for construct
    construct
}


set_construct_version() {
    # Replace symlink for latest
}
