#
# Docker file for MessageInABottle Squad_02 v1.0
#
FROM python:3.8
LABEL maintainer="MessageInABottle Squad_02  API Gateway"
LABEL version="1.0"
LABEL description="MessageInABottle Application Squad_02"

# creating the environment
COPY . /app

# setting the workdir
WORKDIR /app

# installing all requirements
RUN ["pip", "install", "-r", "requirements.prod.txt"]

# exposing the port
EXPOSE 5000/tcp

# Main command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]