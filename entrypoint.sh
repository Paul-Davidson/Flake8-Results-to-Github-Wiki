#!/bin/sh -l

repo_name=$(basename $(git remote get-url origin))

flake8_output=$(flake8 --format json $1)
echo $flake8_outputs

python /entrypoint.py --path-to-wiki-repo $2 --data "$flake8_output"
cp output.md "wiki/${repo_name}-Flake8-Report.md"

echo $repo_name
echo $GITHUB_ACTOR

cd $2
git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"
git add "${repo_name}-Flake8-Report.md"
git commit -m "[bot] Created Flake8 Report for ${repo_name}" --allow-empty
git push -f