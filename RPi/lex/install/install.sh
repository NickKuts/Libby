sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox
sudo apt-get install libatlas-base-dev
sudo apt-get install python-dev
sudo apt-get install python3-dev

pip3 install pyaudio
pip3 install boto3

git clone https://github.com/Kitt-AI/snowboy.git
cd snowboy/swig/Python3
sed -i '5s/.*/SWIG := swig3.0/' Makefile
make
rm Makefile
mv * ../../../../python/snowboy/

cd ../../examples/Python3
mv snowboydecoder.py ../../../../python/snowboy/
# stupid workaround on symbolic links
cp snowboydetect.py s1.py
rm snowboydetect.py
mv s1.py snowboydetect.py
mv snowboydetect.py ../../../../python/snowboy/
cp _snowboydetect.so s1.so
rm _snowboydetect.so
mv s1.so _snowboydetect.so
mv _snowboydetect.so ../../../../python/snowboy/

cd ../../..

rm -r snowboy


cd
mkdir .aws 
cd .aws
printf "[default]\nregion=eu-west-1" > config
printf "[default]\naws_access_key_id = YOUR_ACCESS_KEY\naws_secret_access_key = YOUR_SECRET_KEY" > credentials

