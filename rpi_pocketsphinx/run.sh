docker run \
	-e AWS_DEFAULT_REGION=eu-west-1 \
	-e AWS_ACCESS_KEY_ID=AKIAJLMUJKSJ4ZBYZHEQ \
	-e AWS_SECRET_ACCESS_KEY=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 \
	-e PCM_DEVICE='sysdefault:CARD=USB' \
	--device /dev/snd --privileged \
	libbypi run
