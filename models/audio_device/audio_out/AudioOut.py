from abc import abstractmethod

from models.audio_device.AudioDevice import AudioDevice
from models.sound.Sound import Sound


class AudioOut(AudioDevice):
    @abstractmethod
    def play_audio(self, sound: Sound):
        pass