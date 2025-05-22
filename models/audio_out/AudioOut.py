from abc import ABC, abstractmethod

from models.sound.Sound import Sound


class AudioOut(ABC):
    @abstractmethod
    def play_audio(self, sound: Sound):
        pass