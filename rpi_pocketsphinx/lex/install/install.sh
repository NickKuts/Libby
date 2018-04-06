curl -sSL https://get.docker.com | sh
cd ../../
make
cd lex/install/
bash run.sh
cp docker-Libby.service /etc/systemd/system/
systemctl enable docker-Libby.service
reboot
