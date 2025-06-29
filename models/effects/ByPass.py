from threading import Thread

from models.audio_device.audio_in.AudioIn import AudioIn
from models.audio_device.audio_out.AudioOut import AudioOut
from models.effects.EffectBase import Effect


class ByPass(Effect):
    effect_channel_thread: Thread

    def __init__(self, audio_in: AudioIn, audio_out: AudioOut, volume: int, is_active: bool) -> None:
        super().__init__(volume=volume, is_active=is_active)
        self.effect_channel_thread = Thread(target=self.effect_channel)
        self.audio_in = audio_in
        self.audio_out = audio_out

    def effect_channel(self) -> None:
        try:
            while self.is_active:
                data = self.audio_in.get_audio()
                self.audio_out.play_audio(data)
        finally:
            print("ByPass ended")


    def activate_effect(self) -> None:
        self.is_active = True

        if not self.effect_channel_thread.is_alive():
            self.effect_channel_thread.start()

    def deactivate_effect(self) -> None:
        self.is_active = False
        self.effect_channel_thread.join()