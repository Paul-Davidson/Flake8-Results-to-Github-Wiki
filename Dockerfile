FROM python:3.10-alpine

# ARG check_destination
# ARG wiki_repo

RUN ["apk", "add", "git"]

COPY entrypoint.py /entrypoint.py
COPY requirements.txt /requirements.txt
COPY $check_destination /check

RUN ["pip", "install", "-r", "/requirements.txt"]

RUN ["echo", "$check_destination"]
RUN ["echo", "$wiki_repo"]
RUN ["echo", "$(flake8 --format json /check)"]

ENTRYPOINT ["python", "/entrypoint.py", "--path-to-wiki-repo", "$wiki_repo", "--data", "$(flake8 --format json /check)"]
