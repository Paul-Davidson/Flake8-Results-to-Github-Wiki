FROM python:3.10-alpine

COPY entrypoint.sh /entrypoint.sh
COPY entrypoint.py /entrypoint.py
COPY requirements.txt /requirements.txt

RUN ["apk", "add", "git"]
RUN ["pip", "install", "-r", "/requirements.txt"]

ENTRYPOINT ["/entrypoint.sh"]
