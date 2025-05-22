from abc import ABC, abstractmethod


class AudioDevice(ABC):
    @abstractmethod
    def activate_device(self):
        pass

    @abstractmethod
    def deactivate_device(self):
        pass