import boto3
from subprocess import run, PIPE, CompletedProcess
import wave


class Lex():
    '''
    This class can be used to send voice data to AWS Lex.
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
    Record sound and save it to self.input_fname when silence is detected
    '''
    def record(self):
        f = b''
        process = run(self.sox_command.split(), stdout=PIPE)
        while True:
            output = process.stdout
            if output:
                f += output
            if isinstance(process, CompletedProcess):
                break
        return f

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
        run(['aplay', self.response_fname])
