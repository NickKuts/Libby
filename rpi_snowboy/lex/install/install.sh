sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

#install swig3.0.12, on default ubuntu 16.04 can only install swig3.0.8
# install prerequisite 
sudo apt-get install libpcre3-dev
# download swig 3.0.12
 wget -O swig-3.0.12.tar.gz https://downloads.sourceforge.net/project/swig/swig/swig-3.0.12/swig-3.0.12.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fswig%2Ffiles%2Fswig%2Fswig-3.0.12%2Fswig-3.0.12.tar.gz%2Fdownload&ts=1486782132&use_mirror=superb-sea2

# # extract and configure
tar xf swig-3.0.12.tar.gz
cd swig-3.0.12
./configure --prefix=/usr

# build
make -j 4

# install
sudo make install



sudo apt-get install python-pyaudio python3-pyaudio sox
sudo apt-get install libatlas-base-dev
sudo apt-get install python-dev
sudo apt-get install python3-dev

pip3 install pyaudio
pip3 install boto3

git clone https://github.com/Kitt-AI/snowboy.git
cd snowboy/swig/Python3
# The following line not needed if swig3.0.12 is installed properly
#sed -i '5s/.*/SWIG := swig3.0/' Makefile
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

