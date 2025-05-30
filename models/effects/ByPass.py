import threading
from queue import Queue
from threading import Thread

from models.audio_device.audio_in.AudioIn import AudioIn
from models.audio_device.audio_out.AudioOut import AudioOut
from models.effects.EffectBase import Effect
from models.sound.Sound import Sound


class ByPass(Effect):
    effect_channel_thread: Thread

    def __init__(self, audio_in: AudioIn, audio_out: AudioOut) -> None:
        super().__init__(audio_in=audio_in, audio_out=audio_out)
        self.effect_channel_thread = Thread(target=self.effect_channel)

    def effect_channel(self) -> None:
        while self.is_active:
            data = self.audio_in.get_audio()
            self.audio_out.play_audio(data)


    def activate_effect(self) -> None:
        self.is_active = True

        if not self.effect_channel_thread.is_alive():
            self.effect_channel_thread.start()

        self.effect_channel_thread.join()

    def deactivate_effect(self) -> None:
        pass