ARG BASE=debian
FROM ${BASE}:stretch

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -q -y --no-install-recommends \
    virtualenv git python-pyaudio sox python3-dev build-essential python-dev \
    mpg321 git-core alsa-utils portaudio19-dev python3-pyaudio \
    swig3.0 libatlas-base-dev swig libpulse-dev python3-setuptools \
    python3-setuptools python3-pip rpi.gpio

COPY lex/requirements.txt /rpi/
RUN pip3 install --upgrade wheel setuptools pip
RUN pip3 install --upgrade pocketsphinx==0.1.0
RUN pip3 install -r /rpi/requirements.txt
RUN git clone https://github.com/leachj/vl6180_pi.git
RUN make -C vl6180_pi
RUN make install -C vl6180_pi

COPY lex /rpi/lex

COPY resources/asound.conf.template /etc/asound.conf
COPY resources/entrypoint /

ENTRYPOINT ["/entrypoint"]
