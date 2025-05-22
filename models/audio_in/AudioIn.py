from abc import ABC, abstractmethod


class AudioIn(ABC):
    @abstractmethod
    def get_audio(self):
        pass