FROM python:3.9-alpine

COPY entrypoint.sh /tmp/entrypoint.sh

RUN apk update \
    && apk add build-base

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY code /code
WORKDIR /code

ENTRYPOINT ["/tmp/entrypoint.sh"]
