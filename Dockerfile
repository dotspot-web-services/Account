
# Dockerfile to build glpk container images
# Based on Ubuntu

# Set the base image to Ubuntu
FROM ubuntu:latest

USER root

# Install wget
RUN apt-get update -y && apt-get install -y \
wget \
build-essential \
python3 \
python3-pip \
libpq-dev python3-dev \
--no-install-recommends \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip3 install --trusted-host pypi.python.org pipenv 

WORKDIR /app

COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8
RUN export FLASK_APP=server
ENTRYPOINT ["uwsgi", "uwsgi.ini"]
