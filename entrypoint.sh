#!/bin/sh -l

echo $1
echo $2

flake8_output=$(flake8 --format json $1)
echo $flake8_output

echo $(pwd)
echo $(ls)

python /entrypoint.py --path-to-wiki-repo $2 --data "$flake8_output"
