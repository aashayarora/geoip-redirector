FROM python:3.7-alpine
LABEL maintainer OSG Software <help@opensciencegrid.org>

WORKDIR /code

COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install -r requirements.txt

ENV FLASK_APP=geoip.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
