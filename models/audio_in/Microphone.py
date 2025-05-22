from models.audio_in.AudioIn import AudioIn
from soundcard import _Microphone

from models.sound.Sound import Sound

class Microphone(AudioIn):
    microphone: _Microphone
    rate: int
    chunk: int

    def __init__(self, microphone: _Microphone, rate: int=96000, chunk: int=8152):
        self.microphone = microphone
        self.rate = rate
        self.chunk = chunk

    def get_audio(self) -> Sound:
        with self.microphone.recorder(samplerate=self.rate) as mic:
            data = mic.record(numframes=self.chunk)
            sound = Sound(data)
            return sound


