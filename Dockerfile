FROM openconceptlab/oclweb-dependencies:1.0.0

ADD . /code/
WORKDIR /code

EXPOSE 7000

CMD bash startup.sh