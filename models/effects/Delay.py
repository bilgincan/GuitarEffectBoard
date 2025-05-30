import threading
from threading import Thread

from models.audio_device.audio_in import AudioIn
from models.audio_device.audio_out import AudioOut
from models.effects.EffectBase import Effect
from multiprocessing import Process, Queue

from models.sound.Sound import Sound


class Delay(Effect):
    delay_rate: int
    frequency: int
    effect_channel_thread: Thread
    sampler: Thread

    def __init__(self, audio_in: AudioIn, audio_out: AudioOut, delay_rate: int=15, frequency: int=25):
        super().__init__(audio_in=audio_in, audio_out=audio_out)
        self.delay_rate = delay_rate
        self.frequency = frequency
        self.effect_channel_thread = Thread(target=self.effect_channel)

    def effect_channel(self) -> None:
        q = Queue()
        self.sampler = threading.Thread(target=self.create_samples, args=(q, self.delay_rate))
        self.sampler.start()

        while self.is_active:
            threads = []

            for _ in range(self.frequency):
                t = threading.Thread(target=self.delay, args=(q,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

        self.sampler.join()

    def delay(self, q: Queue) -> None:
        samples = q.get()

        for sample in samples:
            sound = Sound(sample)
            self.audio_out.play_audio(sound)

    def create_samples(self, q: Queue, sample_limit=15) -> None:
        samples = []
        i = 0

        while self.is_active:
            sample_sound: Sound = self.audio_in.get_audio()
            samples.append(sample_sound.sample)
            q.put(samples)

            if i == sample_limit:
                samples = []
                i = 0
            i = i + 1

    def activate_effect(self) -> None:
        self.is_active = True

        if not self.effect_channel_thread.is_alive():
            self.effect_channel_thread.start()

        self.effect_channel_thread.join()

    def deactivate_effect(self) -> None:
        self.is_active = False
