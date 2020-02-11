FROM python:3.8.1-buster

RUN apt-get -qq update && apt-get -qq install vim

COPY ./ /museums

RUN cd museums && pip install -q -r requirements.txt

RUN cd museums && python fetch.py
ENTRYPOINT  ["/bin/bash"]
