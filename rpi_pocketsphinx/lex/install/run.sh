docker run\
    -e PCM_DEVICE='sysdefault:CARD=USB' \
    --device /dev/snd --privileged \
    libbypi:latest run
