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
    by_pass_channel: Process
    effect_channel: Process
    sampler: Thread

    def __init__(self, audio_in: AudioIn, audio_out: AudioOut, delay_rate: int=15, frequency: int=25):
        super().__init__(audio_in=audio_in, audio_out=audio_out)
        self.delay_rate = delay_rate
        self.frequency = frequency

    def effect_channel(self) -> None:
        q = Queue()
        self.sampler = threading.Thread(target=self.create_samples, args=(q, self.delay_rate))
        self.sampler.start()

        while True:
            threads = []

            for _ in range(self.frequency):
                t = threading.Thread(target=self.delay, args=(q,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

    def delay(self, q: Queue) -> None:
        samples = q.get()
        sound = Sound(samples)
        super().audio_out.play_audio(sound)

    def create_samples(self, q: Queue, sample_limit=15) -> None:
        samples = []
        i = 0

        while True:
            sample_sound = super().audio_in.get_audio()
            samples.append(sample_sound)
            q.put(samples)

            if i == sample_limit:
                samples = []
                i = 0
            i = i + 1

    def activate_effect(self) -> None:
        self.by_pass_channel = Process(target=super().bypass_channel)
        self.effect_channel = Process(target=self.effect_channel)

        self.by_pass_channel.start()
        self.effect_channel.start()
        self.is_active = True

        self.by_pass_channel.join()
        self.effect_channel.join()

    def deactivate_effect(self) -> None:
        self.is_active = False
        self.effect_channel.terminate()