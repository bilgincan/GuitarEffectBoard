from models.audio_out.AudioOut import AudioOut
from models.sound.Sound import Sound
from soundcard import _Speaker


class Speaker(AudioOut):
    speaker: _Speaker
    rate: int
    chunk: int

    def __init__(self, speaker: _Speaker, rate: int, chunk: int):
        self.speaker = speaker
        self.rate = rate
        self.chunk = chunk

    def play_audio(self, sound: Sound):
        with self.speaker.player(samplerate=self.rate) as audio_output:
            for sample in sound.samples:
                audio_output.play(sample)