from abc import abstractmethod

from models.audio_device.AudioDevice import AudioDevice


class AudioIn(AudioDevice):
    @abstractmethod
    def get_audio(self):
        pass