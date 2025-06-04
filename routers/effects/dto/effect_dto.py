from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import Type, Dict

from models.audio_device.audio_in.AudioIn import AudioIn
from models.audio_device.audio_out.AudioOut import AudioOut
from models.effects.ByPass import ByPass
from models.effects.Delay import Delay
from models.effects.EffectBase import Effect
from routers.effects.dto.effect_type_enum import EffectType

effect_dto_registry: Dict[Type['Effect'], Type['EffectDto']] = {}

class EffectDto(BaseModel):
    volume: int
    is_active: bool
    effect_type: EffectType
    delay_rate: int = 0
    frequency: int = 0

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> Effect:
        pass

    @classmethod
    def register_effect(cls, effect_cls: Type['Effect']):
        def wrapper(dto_cls: Type['EffectDto']):
            effect_dto_registry[effect_cls] = dto_cls
            return dto_cls

        return wrapper

    @staticmethod
    def reverse_map(effect: 'Effect') -> 'EffectDto':
        dto_cls = effect_dto_registry.get(type(effect))
        if dto_cls is None:
            return NonEffectDto.reverse_map(effect)
        return dto_cls.reverse_map(effect)

class NonEffectDto(EffectDto):

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> Effect:
        return ByPass(audio_in=audio_in, audio_out=audio_out)

    @staticmethod
    def reverse_map(effect: Effect):
        return NonEffectDto(volume=0, is_active=False, effect_type=EffectType.NON_EFFECT)

@EffectDto.register_effect(Delay)
class DelayDto(EffectDto):
    delay_rate: int
    frequency: int

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> Delay:
        return Delay(audio_in=audio_in, audio_out=audio_out, frequency=self.frequency, delay_rate=self.delay_rate, volume=self.volume, is_active=self.is_active)

    @staticmethod
    def reverse_map(effect: Delay) -> 'DelayDto':
        return DelayDto(volume=effect.volume, is_active=effect.is_active, frequency=effect.frequency, delay_rate=effect.delay_rate, effect_type=EffectType.DELAY)

@EffectDto.register_effect(ByPass)
class ByPassDto(EffectDto):

    def map(self, audio_in: AudioIn, audio_out: AudioOut) -> ByPass:
        return ByPass(audio_in=audio_in, audio_out=audio_out, volume=self.volume, is_active=self.is_active)

    @staticmethod
    def reverse_map(effect: Effect) -> 'ByPassDto':
        return ByPassDto(volume=effect.volume, is_active=effect.is_active, effect_type=EffectType.BYPASS)