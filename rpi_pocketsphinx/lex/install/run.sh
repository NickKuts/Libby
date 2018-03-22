docker run\
    -e AWS_DEFAULT_REGION= \
    -e AWS_ACCES_KEY_ID= \
    -e AWS_SECRET_ACCESS_KEY= \
    -e PCM_DEVICE='sysdefault:CARD=USB' \
    --device /dev/snd --privileged \
    libbypi:latest run
