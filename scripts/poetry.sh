#!/bin/bash

set -e

scripts/run.sh --no-deps --user root web poetry "$@"
