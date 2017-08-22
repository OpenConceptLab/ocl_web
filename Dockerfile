FROM python:2.7.13
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
ADD . /code/
WORKDIR /code
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install curl
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash
RUN apt-get -y install nodejs 

RUN npm install
RUN npm install -g grunt-cli

EXPOSE 7000

CMD bash startup.sh