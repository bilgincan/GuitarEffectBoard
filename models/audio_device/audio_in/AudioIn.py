from abc import abstractmethod

from models.audio_device.AudioDevice import AudioDevice
from models.sound.Sound import Sound


class AudioIn(AudioDevice):
    @abstractmethod
    def get_audio(self) -> Sound:
        pass