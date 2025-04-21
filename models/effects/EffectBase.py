from abc import ABC, abstractmethod
import soundcard as sc
from soundcard import _Microphone, _Speaker


class Effect(ABC):
    volume: int
    is_active: bool
    audio_in:  _Microphone
    audio_out: _Speaker
    rate: int
    chunk: int

    def __init__(self, volume: int=50, is_active: bool=True, audio_in: _Microphone=sc.default_microphone(), audio_out: _Speaker=sc.default_speaker(), rate: int=96000, chunk: int=8152):
        self.volume = volume
        self.is_active = is_active
        self.audio_out = audio_out
        self.audio_in = audio_in
        self.rate = rate
        self.chunk = chunk

    def bypass_channel(self) -> None:
        with self.audio_in.recorder(samplerate=self.rate) as mic, self.audio_out.player(samplerate=self.rate) as audio_output:
            while True:
                data = mic.record(numframes=self.chunk)
                audio_output.play(data)

    @abstractmethod
    def effect_channel(self) -> None:
        pass

    @abstractmethod
    def activate_effect(self) -> None:
        pass

    @abstractmethod
    def deactivate_effect(self) -> None:
        pass


