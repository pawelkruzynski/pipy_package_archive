FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD requirements.txt /config/
RUN apt-get -y update && \
    apt-get install -y inotify-tools && \
    pip install --upgrade pip && \
    pip install -r /config/requirements.txt

RUN mkdir /src && \
    mkdir /src/static && \
    mkdir /src/postgres;
WORKDIR /src
RUN echo "alias ll='ls -l --color=auto'" >> ~/.bashrc
