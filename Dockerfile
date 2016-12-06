FROM ubuntu:16.04

WORKDIR /opt/ownCA
ADD . .
RUN apt-get update
RUN apt-get install -y python-pip
RUN apt-get install -y libssl-dev
RUN pip install -r requirements.txt
RUN chmod a+x start.sh

EXPOSE 80

VOLUME database
VOLUME certs/migrations

CMD /opt/ownCA/start.sh
