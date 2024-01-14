FROM python:3.10-alpine

ARG check-destination
ARG wiki-repo

RUN apk add git

COPY entrypoint.py /entrypoint.py
COPY requirements.txt /requirements.txt
COPY $destination /check

RUN pip install -r /requirements.txt

RUN echo $check-destination
RUN echo $wiki-repo
RUN echo $(flake8 --format json /check)

ENTRYPOINT python /entrypoint.py --path-to-wiki-repo $wiki-repo --data $(flake8 --format json /check)
