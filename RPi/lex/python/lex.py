import boto3
from subprocess import run, Popen
import wave
import os

'''
This class can be used to send voice data to AWS Lex.
'''
class Lex():
    def __init__(self):
        self.client = boto3.client('lex-runtime')
        self.bot_name = 'Libby'
        self.bot_alias = 'Dev'
        self.user_id = 'lexpi'
        self.content_type = 'audio/l16; rate=16000; channels=1'
        self.input_stream = b''
        self.input_fname = 'request.wav'
        self.response_fname = 'response.wav'
        self.sox_command = 'sox -d -t wavpcm -c 1 -b 16 -r 16000 -e signed-integer --endian little - silence 1 0 6% 5 0.275t 7% > ' + self.input_fname


    '''
    Record sound and save it to self.input_fname when silence is detected
    '''
    def record(self):
        os.system(self.sox_command)
        #Popen(self.sox_command.split())
        '''
        Uncomment this if you want to play back the recording before
        sending it to Lex
        '''
        #os.system('sox ' + self.input_fname + ' -d')

    def create_input_stream(self):
        print("Creating input stream from", self.input_fname)
        stream = open(self.input_fname, 'rb')
        data = stream
        return data

    def post_content(self):
        try:
            data = self.create_input_stream()
            response = self.client.post_content(
                botName=self.bot_name,
                botAlias=self.bot_alias,
                userId=self.user_id,
                contentType=self.content_type,
                inputStream=data
            )
        finally:
            pass
            #data.close()

        print(response)
        return response

    '''
    Play back the response's audio stream
    '''
    def play_response(self, response):
        audio_stream = response['audioStream'].read()
        response['audioStream'].close()

        f = wave.open(self.response_fname, 'wb')
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.setnframes(0)

        f.writeframesraw(audio_stream)
        f.close()
        run(['mpg321', self.response_fname])

