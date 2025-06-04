from pydantic import BaseModel

from models.audio_device.audio_in.AudioIn import AudioIn
from models.audio_device.audio_out.AudioOut import AudioOut
from models.effects.ByPass import ByPass
from models.effects.Delay import Delay
from models.effects.EffectBase import Effect
from routers.effects.dto.effect_type_enum import EffectType


class EffectDto(BaseModel):
    volume: int
    is_active: bool
    effect_type: EffectType
    delay_rate: int = 0
    frequency: int = 0

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> Effect:
        pass

    @staticmethod
    def reverse_map(effect: Effect):
        if isinstance(effect, Delay):
            return DelayDto.reverse_map(effect=effect)
        elif isinstance(effect, ByPass):
            return ByPassDto.reverse_map(effect=effect)
        else:
            return NonEffectDto.reverse_map(effect=effect)

class NonEffectDto(EffectDto):

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> Effect:
        return ByPass(audio_in=audio_in, audio_out=audio_out)

    @staticmethod
    def reverse_map(effect: Effect):
        return NonEffectDto(volume=0, is_active=False, effect_type=EffectType.NON_EFFECT)

class DelayDto(EffectDto):
    delay_rate: int
    frequency: int

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> Effect:
        return Delay(audio_in=audio_in, audio_out=audio_out, frequency=self.frequency, delay_rate=self.delay_rate, volume=self.volume, is_active=self.is_active)

    @staticmethod
    def reverse_map(effect: Delay):
        return DelayDto(volume=effect.volume, is_active=effect.is_active, frequency=effect.frequency, delay_rate=effect.delay_rate, effect_type=EffectType.DELAY)

class ByPassDto(EffectDto):

    def map(self, audio_in: AudioIn, audio_out: AudioOut):
        return ByPass(audio_in=audio_in, audio_out=audio_out, volume=self.volume, is_active=self.is_active)

    @staticmethod
    def reverse_map(effect: Effect):
        return ByPassDto(volume=effect.volume, is_active=effect.is_active, effect_type=EffectType.BYPASS)