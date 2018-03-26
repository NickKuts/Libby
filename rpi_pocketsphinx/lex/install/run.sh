docker run\
    -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
    -e AWS_ACCES_KEY_ID=${AWS_ACCES_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    -e PCM_DEVICE='sysdefault:CARD=USB' \
    --device /dev/snd \
    --name=PROJECT_LIBBY
    libbypi:latest run
