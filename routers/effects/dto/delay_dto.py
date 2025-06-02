from models.effects.Delay import Delay
from models.effects.EffectBase import Effect
from routers.effects.dto.effect_dto import EffectDto


class DelayDto(EffectDto):
    delay_rate: int
    frequency: int

    def map(self) -> Effect:
        return Delay(audio_in=self.audio_in, audio_out=self.audio_out, frequency=self.frequency, delay_rate=self.delay_rate)
