from abc import ABC

from bson import ObjectId
from typing import Type, Dict

from repository.BaseModel import BaseModel
from models.effects.Delay import Delay
from models.effects.ByPass import ByPass
from models.effects.EffectBase import Effect

effect_registry: Dict[Type['Effect'], Type['EffectBaseModel']] = {}

class EffectBaseModel(BaseModel, ABC):
    board_id: ObjectId
    volume: int
    is_active: bool

    @classmethod
    def register_effect(cls, effect_cls: Type['Effect']):
        def wrapper(dto_cls: Type['EffectBaseModel']):
            effect_registry[effect_cls] = dto_cls
            return dto_cls

        return wrapper

    @staticmethod
    def reverse_map(base_object: 'Effect') -> 'EffectBaseModel':
        cls = effect_registry.get(type(base_object))
        if cls is None:
            default_effect: ByPass = ByPass(volume=50, is_active=False, audio_in=None, audio_out=None)
            return ByPassModel.reverse_map(default_effect)
        return cls.reverse_map(base_object)

@EffectBaseModel.register_effect(Delay)
class DelayModel(EffectBaseModel):
    delay_rate: int
    frequency: int

    @staticmethod
    def reverse_map(delay: Effect) -> 'EffectBaseModel':
        db_model_obj = DelayModel()

        db_model_obj.volume = delay.volume
        db_model_obj.is_active = delay.is_active
        db_model_obj.delay_rate = delay.delay_rate
        db_model_obj.frequency = delay.frequency

        return db_model_obj

    def map(self):
        pass

@EffectBaseModel.register_effect(ByPass)
class ByPassModel(EffectBaseModel):
    @staticmethod
    def reverse_map(base_object: Effect) -> 'EffectBaseModel':
        db_model_obj = ByPassModel()
        db_model_obj.volume = base_object.volume
        db_model_obj.is_active = base_object.is_active

        return db_model_obj

    def map(self):
        pass

