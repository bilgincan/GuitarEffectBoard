import random

from models.audio_device.audio_in.AudioIn import AudioIn
import numpy as np

from models.sound.Sound import Sound


class SampleAudioGenerator(AudioIn):
    def activate_device(self):
        pass

    def deactivate_device(self):
        pass

    duration: float # seconds
    frequency: float  # Hz (A4)
    sample_rate: int  # Samples per second (standard audio rate)

    def __init__(self, duration: float=1.0, frequency: float=440.0, sample_rate: int=44100):
        self.duration = duration
        self.frequency = frequency
        self.sample_rate = sample_rate

    def get_audio(self) -> Sound:
        #change frequency at each time
        # Generate a random integer between -100 and 100
        random_number = random.randint(-100, 100)

        frequency_used = self.frequency + random_number

        # Generate the time axis
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

        # Generate the sine wave
        audio = 0.5 * np.sin(2 * np.pi * frequency_used * t)
        return Sound(audio)