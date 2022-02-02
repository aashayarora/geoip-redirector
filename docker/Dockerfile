FROM python:3.7-alpine
LABEL maintainer Aashay Arora <aaarora@ucsd.edu>

WORKDIR /code

COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install -r requirements.txt

COPY app/* /code/

ENV FLASK_APP=geoip.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
