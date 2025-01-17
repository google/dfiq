#!/bin/bash
set -e

PYTHONPATH="/app"

# Run the container the default way
if [[ "$1" =~ 'envshell' ]]; then
    poetry shell
fi

# Run a custom command on container start
exec "$@"
