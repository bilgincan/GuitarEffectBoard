from abc import ABC, abstractmethod

from models.audio_device.audio_in import AudioIn
from models.audio_device.audio_out import AudioOut
from models.sound.Sound import Sound


class Effect(ABC):
    volume: int
    is_active: bool
    audio_in:  AudioIn
    audio_out: AudioOut

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


