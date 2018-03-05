docker run\
    -e AWS_DEFAULT_REGION=eu-west-1 \
    -e AWS_ACCESS_KEY_ID=AKIAJSY4GPTL3VRDR3NQ \
    -e AWS_SECRET_ACCESS_KEY=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 \
    -e PCM_DEVICE='sysdefault:CARD=USB' \
    --device /dev/snd --privileged \
    libbypi:latest run
