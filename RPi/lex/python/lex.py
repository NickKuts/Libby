import boto3
from subprocess import run, PIPE, CompletedProcess
import wave


class Lex():
    '''
    This class can be used to send voice data to AWS Lex.
<<<<<<< HEAD
=======
    The credentials for aws are loaded from ~/.aws/credentials
    and region from ~/.aws/region
>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6
    '''
    def __init__(self):
        self.client = boto3.client('lex-runtime')
        self.bot_name = 'Libby'
        self.bot_alias = 'Dev'
        self.user_id = 'lexpi'
        self.content_type = 'audio/l16; rate=16000; channels=1'
        self.input_stream = b''
        self.input_fname = 'request.wav'
        self.response_fname = 'response.wav'
        self.sox_command = 'sox -d -t wavpcm -c 1 -b 16 -r 16000 -e signed-integer --endian little - silence 1 0 6% 5 0.275t 7%'

    '''
    Create a stream while recording and return it
    '''
    def record(self):
        f = b''
        process = run(self.sox_command.split(), stdout=PIPE)
<<<<<<< HEAD
        while not isinstance(process, CompletedProcess):
            output = process.stdout
            if output:
                f += output
        return f
        '''
        Uncomment this if you want to play back the recording before
        sending it to Lex
        '''
        # os.system('sox ' + self.input_fname + ' -d')

    def post_content(self):
        try:
            data = self.record()
            response = self.client.post_content(
                botName=self.bot_name,
                botAlias=self.bot_alias,
                userId=self.user_id,
                contentType=self.content_type,
                inputStream=data
            )
        finally:
            pass
=======
        while True:
            output = process.stdout
            if output:
                f += output
            if isinstance(process, CompletedProcess):
                break
        return f

    def post_content(self):
        data = self.record()
        response = self.client.post_content(
            botName=self.bot_name,
            botAlias=self.bot_alias,
            userId=self.user_id,
            contentType=self.content_type,
            inputStream=data
        )
>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6

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
<<<<<<< HEAD
        run(['aplay', self.response_fname])
=======
        run(['mpg321', self.response_fname])

        state = response['dialogState']
        return state


>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6
