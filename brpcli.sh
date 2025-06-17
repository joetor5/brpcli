#!/usr/bin/env bash
# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

if [[ -d brpcli && -d .git ]]; then
    BRPCLI="python3 brpcli/cli.py"
    PYVENV=".venv/bin/activate"
else
    BRPCLI="brpcli"
    PYVENV="$HOME/.brpcli/.venv/bin/activate"
fi

source $PYVENV
clear
$BRPCLI "$@"

