curl -sSL https://get.docker.com | sh
cd ../../
make
cd lex/install/
script="docker run\
    -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e PCM_DEVICE='sysdefault:CARD=USB' \
    --device /dev/snd --privileged\
    libbypi:latest run"
touch run.sh
echo $script > run.sh
bash run.sh
cp docker-Libby.service /etc/systemd/system/
systemctl enable docker-Libby.service
reboot
