from abc import ABC, abstractmethod
import soundcard as sc
from soundcard import _Microphone, _Speaker

from models.audio_in.AudioIn import AudioIn
from models.audio_out.AudioOut import AudioOut
from models.sound.Sound import Sound


class Effect(ABC):
    volume: int
    is_active: bool
    audio_in:  AudioIn
    audio_out: AudioOut

    #audio_in: _Microphone = sc.default_microphone(), audio_out: _Speaker = sc.default_speaker()

    def __init__(self, audio_in: AudioIn, audio_out: AudioOut, volume: int=50, is_active: bool=True):
        self.volume = volume
        self.is_active = is_active
        self.audio_out = audio_out
        self.audio_in = audio_in

    def bypass_channel(self) -> None:
        while True:
            data: Sound = self.audio_in.get_audio()
            self.audio_out.play_audio(data)

    @abstractmethod
    def effect_channel(self) -> None:
        pass

    @abstractmethod
    def activate_effect(self) -> None:
        pass

    @abstractmethod
    def deactivate_effect(self) -> None:
        pass


