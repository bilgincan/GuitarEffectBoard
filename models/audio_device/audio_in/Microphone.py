from models.audio_device.audio_in.AudioIn import AudioIn

from models.sound.Sound import Sound

class Microphone(AudioIn):
    microphone: any # _Microphone in soundcard
    device: any # _Recorder in soundcard
    rate: int
    chunk: int

    def __init__(self, microphone: any, rate: int=96000, chunk: int=8152):
        self.microphone = microphone
        self.rate = rate
        self.chunk = chunk
        self.device = None

    def get_audio(self) -> Sound:
        with self.microphone.recorder(samplerate=self.rate) as mic:
            data = mic.record(numframes=self.chunk)
            sound = Sound(data)
            return sound

    def deactivate_device(self):
        self.device.flush()

    def activate_device(self):
        with self.microphone.recorder(samplerate=self.rate) as mic:
            self.device = mic
            return mic
