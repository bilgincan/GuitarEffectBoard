from models.audio_device.audio_out.AudioOut import AudioOut
from models.sound.Sound import Sound


class Speaker(AudioOut):
    speaker: any # _Speaker in soundcard
    device: any # _Player in soundcard
    rate: int
    chunk: int

    def __init__(self, speaker: any, rate: int=96000, chunk: int=8152):
        self.speaker = speaker
        self.rate = rate
        self.chunk = chunk
        self.device = None

    def play_audio(self, sound: Sound):
        if self.device is None:
            self.activate_device()

        for sample in sound.samples:
            self.device.play(sample)

    def activate_device(self):
        with self.speaker.player(samplerate=self.rate) as audio_output:
            self.device = audio_output

    def deactivate_device(self):
        pass