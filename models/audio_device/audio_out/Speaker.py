from models.audio_device.audio_out.AudioOut import AudioOut
from models.sound.Sound import Sound


class Speaker(AudioOut):
    speaker: any # _Speaker in soundcard
    rate: int
    chunk: int

    def __init__(self, speaker: any, rate: int=96000, chunk: int=8152):
        self.speaker = speaker
        self.rate = rate
        self.chunk = chunk
        self.device = None

    def play_audio(self, sound: Sound):
        with self.speaker.player(samplerate=self.rate) as audio_output:
             audio_output.play(sound.sample)

    def activate_device(self):
        with self.speaker.player(samplerate=self.rate) as audio_output:
            return audio_output

    def deactivate_device(self):
        pass