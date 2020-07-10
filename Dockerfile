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
RUN apk add --no-cache mariadb-dev build-base jpeg-dev zlib-dev

#Upgrade pip
RUN pip install pip -U
ADD requirements.txt /app/

#Install dependencies
RUN pip install -r requirements.txt
ADD . /app/

# collect static files
RUN python manage.py collectstatic --noinput

#run migrate
RUN python manage.py migrate

# add and run as non-root user
RUN adduser -D devph
USER devph

# run gunicorn
CMD gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
