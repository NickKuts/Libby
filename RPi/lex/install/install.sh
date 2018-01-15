sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox
sudo apt-get install libatlas-base-dev
pip3 install pyaudio
pip3 install boto3
cd
mkdir .aws 
cd .aws
printf "[default]\nregion=eu-west-1" > config
printf "[default]\naws_access_key_id = YOUR_ACCESS_KEY\naws_secret_access_key = YOUR_SECRET_KEY" > credentials

