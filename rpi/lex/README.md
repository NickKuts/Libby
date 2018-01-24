
## Amazon Lex client

This is the Amazon Lex client. Basically it is a program that you leave running that recognizes when you say Libby and then starts recording voice. When the user has finished his/her sentence, the client sends the data to Libby bot which then uses Libby or LibbyDev lambda function to create a response. The response is sent back to the client which then plays it and depending on the response's type starts assumes the conversation finished or starts waiting for more input.

The client is made with Python3 and uses Amazon SDK boto3 to communicate with AWS. 

For wakeword detection, the client uses [Snowboy](https://snowboy.kitt.ai/).  

## Manual installation with install.sh (no docker)

Installation:
```
git clone https://github.com/NickKuts/Libby/tree/develop
cd Libby
git checkout develop
cd rpi/lex/install
./install.sh
cd ..
cd python
```

Please note that you need modify the /.aws/credential file with your AWS user credentials.
You can find your acces key and secret access key from aws. From top right click your user name and select ‘My Security Credentials’. Then from the left select ‘Users’ and your click your name. Then select the tab ‘Security credentials’ and create a new access key.

After configuring your aws credentials, you can run the client in the Libby/rpi/lex/python directory with
```
python3 run.py
```
In case you wish to use only the client without snowboy wakeword detection, you can run

```
python3 run_no_snowboy.py
```

The installation script first installs the required libraries, then clones snowboy repository, builds the python3 version of snowboy, moves the built files to the lex working directory and then removes the snowboy repository.

The javascript implementation does not have an installation script, but in case you need to use it, you can follow the guide in https://aws.amazon.com/blogs/machine-learning/build-a-voice-kit-with-amazon-lex-and-a-raspberry-pi/

## Installing an existing docker image from the registry

For deployment.  No libby source code required.  Just install docker:

```
curl -sSL https://get.docker.com | sh
systemctl start docker
```

Pull one the pre-built images, depending on platform:

```
repo=263893614267.dkr.ecr.eu-west-1.amazonaws.com
docker pull $repo/libbypi:raspbian    # on Raspberry Pi
docker pull $repo/libbypi:x86_64      # not on Raspberry Pi
```

Run a container:

```
docker run $repo/libbypi:XXX help
```

The help option show instructions on how to run it in real use:

```
libbypi docker container

USAGE:
    docker run \
        -e AWS_DEFAULT_REGION=eu-west-1 \
        -e AWS_ACCESS_KEY_ID=... \
        -e AWS_SECRET_ACCESS_KEY=... \
        --device /dev/snd --privileged \
        [-i -t] libbypi MODE

where MODE is one of
  - run
  - run_no_snowboy
  - help (prints this message)
  - shell (requires -i -t to be usable)
```

## Rebuilding the docker image

Clone libby.  Then:

```
cd rpi
make
```

And proceed with "docker run" like with a downloaded image:

```
docker run libbypi help
```

To tag and push this local image to the ECR registry for other users,
run "make push".

TODO: currently there is only one tag per platform.  Better release
discipline might be to have separate develop and master tags, or even
better, version numbers.
