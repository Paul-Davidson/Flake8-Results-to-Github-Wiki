#!/bin/sh -l

repo_name=${GITHUB_REPOSITORY#*/}

python_module_file="$1/__init__.py"
if [ -f "$python_module_file" ]; then
    repo_name=${python_module_file#*/}
fi

git config --global --add safe.directory "$GITHUB_WORKSPACE"
git config --global --add safe.directory "$GITHUB_WORKSPACE/$2"

flake8_output=$(flake8 --format json $1)

python /entrypoint.py --path-to-wiki-repo $2 --data "$flake8_output"
cp output.md "$2/${repo_name}-Flake8-Report.md"

cd $2

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git add "${repo_name}-Flake8-Report.md"
git commit -m "[bot] Created Flake8 Report for ${repo_name}" --allow-empty
git push -f