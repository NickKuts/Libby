ARG BASE=debian
FROM ${BASE}:stretch

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -q -y --no-install-recommends \
    virtualenv git python-pyaudio sox python3-dev build-essential python-dev \
    mpg321 git-core alsa-utils portaudio19-dev python3-pyaudio \
    swig3.0 libatlas-base-dev swig


COPY lex/requirements.txt /rpi/
RUN virtualenv -p python3 /venv && \
    /venv/bin/pip install -r /rpi/requirements.txt

COPY lex /rpi/lex

RUN cd /rpi/lex/python && \
    git clone https://github.com/cmusphinx/pocketsphinx && \
    git clone https://github.com/cmusphinx/sphinxbase && \
    cd pocketsphinx-python && \
    python setup.py install
COPY resources/asound.conf.template /etc/asound.conf
COPY resources/entrypoint /

ENTRYPOINT ["/entrypoint"]
