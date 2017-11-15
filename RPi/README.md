# Raspberry Pi Setup
## Running the script
Remember to make the file executable first:
```
chmod +x rasp_setup.sh
```

Additional stuff to do before AlexaPi works:
If errors arise, this could be useful https://github.com/alexa-pi/AlexaPi/wiki/Audio-setup-&-debugging

Also recommended to run Alexa via debugging (https://github.com/alexa-pi/AlexaPi/wiki/Debugging#debug-mode), with this command
$ sudo systemctl stop AlexaPi.service
$ /opt/AlexaPi/src/main.py -d


0.
Read from here:
https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=169622
Test that microphone is working:
arecord -f cd -D hw:1,0 -d 10 test.wav
You can play that with aplay


1.
Read from here:
https://raspberrypi.stackexchange.com/questions/37177/best-way-to-setup-usb-mic-as-system-default-on-raspbian-jessie

Now, to set the USB sound card to your default card you will need to edit the file /usr/share/alsa/alsa.conf with the command sudo nano /usr/share/alsa/alsa.conf scroll down until you find the lines

defaults.ctl.card 0
defaults.pcm.card 0

and change them to

defaults.ctl.card 1
defaults.pcm.card 1


2.
Read from here:
https://github.com/alexa-pi/AlexaPi/issues/265


    If you're using VLC handler set

    sudo nano /etc/opt/AlexaPi/config.yaml

    input_device: "pulse"
    output: "pulse"
    output_device: ""

    Download VLC manually using this 'sudo apt-get install vlc'
    $ sudo apt-get install vlc
    $ reboot



Issues that might be related and useful:
https://github.com/alexa-pi/AlexaPi/issues/343
https://github.com/alexa-pi/AlexaPi/issues/335
