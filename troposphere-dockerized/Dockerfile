FROM python:3.9-slim-buster

LABEL maintainer="allan@cryptelic.com"

WORKDIR /troposphere

RUN apt-get -qq update && apt-get install -y build-essential libssl-dev groff \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["pip", "freeze"]

