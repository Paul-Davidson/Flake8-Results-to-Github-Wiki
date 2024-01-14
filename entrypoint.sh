#!/bin/sh -l

flake8_output=$(flake8 --format json $1)
echo $flake8_output
python /entrypoint.py --path-to-wiki-repo $2 --data $1
