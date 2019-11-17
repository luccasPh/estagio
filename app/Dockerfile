# Pull the base image
FROM python:3.7-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

#MySQL development headers and libraries
RUN apk update
RUN apk add python3-dev 
RUN apk add --no-cache mariadb-dev build-base

#Upgrade pip
RUN pip install pip -U
ADD requirements.txt /app/

#Install dependencies
RUN pip install -r requirements.txt
ADD . /app/

