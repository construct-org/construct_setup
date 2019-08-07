#!/bin/bash

_tmpdir=$(mktemp -d)
export SCRIM_PATH="$_tmpdir/scrim_out.sh"

python -m install "$@"

if [ -e "$SCRIM_PATH" ]; then

    source "$SCRIM_PATH"

    if [ $? -ne 0 ]; then
        echo "Error:"
        echo ""
        cat $SCRIM_PATH
        echo
    fi

fi

unset SCRIM_PATH
rm -rf $_tmpdir
