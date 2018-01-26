ARG BASE=debian
FROM ${BASE}:stretch

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -q -y --no-install-recommends \
        swig3.0 python-pyaudio python3-pyaudio sox libatlas-base-dev \
        python-dev python3-dev virtualenv build-essential portaudio19-dev \
        git-core mpg321 alsa-utils

COPY lex/requirements.txt /rpi/
RUN virtualenv -p python3 /venv && \
    /venv/bin/pip install -r /rpi/requirements.txt
# Workaround to recover snowboydetect.py, which setup.py fails to install:
RUN make -C venv/src/snowboy/swig/Python3 SWIG=swig3.0

COPY lex /rpi/lex
RUN tar C /venv/src/snowboy -cf - \
   swig/Python3/_snowboydetect.so \
   swig/Python3/snowboydetect.py \
   examples/Python3/snowboydecoder.py \
   | tar C /rpi/lex/python/snowboy --strip=2 -xvf -

COPY resources/asound.conf /etc/
COPY resources/entrypoint /

ENTRYPOINT ["/entrypoint"]
