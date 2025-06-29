from abc import ABC

from bson import ObjectId
from typing import Type, Dict

from models.effects.NoneTypeEffect import NoneTypeEffect
from repository.BaseModel import BaseModel
from models.effects.Delay import Delay
from models.effects.ByPass import ByPass
from models.effects.EffectBase import Effect

effect_registry: Dict[Type['Effect'], Type['EffectBaseModel']] = {}

class EffectBaseModel(BaseModel, ABC):
    board_id: ObjectId
    volume: int
    is_active: bool
    effect_type: str

    @classmethod
    def register_effect(cls, effect_cls: Type['Effect']):
        def wrapper(dto_cls: Type['EffectBaseModel']):
            effect_registry[effect_cls] = dto_cls
            return dto_cls

        return wrapper

    @staticmethod
    def reverse_map(base_object: 'Effect') -> 'EffectBaseModel':
        cls = effect_registry.get(type(base_object))
        return cls.reverse_map(base_object)

@EffectBaseModel.register_effect(NoneTypeEffect)
class NoneTypeEffectModel(EffectBaseModel):
    effect_type: str = "NoneTypeEffect"

    @staticmethod
    def reverse_map(base_object: NoneTypeEffect) -> 'EffectBaseModel':
        db_model_obj = NoneTypeEffectModel()
        db_model_obj.effect_type = "NoneTypeEffect"
        return db_model_obj

    def map(self):
        pass


@EffectBaseModel.register_effect(Delay)
class DelayModel(EffectBaseModel):
    effect_type: str = "Delay"
    delay_rate: int
    frequency: int

    @staticmethod
    def reverse_map(delay: Delay) -> 'EffectBaseModel':
        db_model_obj = DelayModel()
        db_model_obj.effect_type = "Delay"

        db_model_obj.volume = delay.volume
        db_model_obj.is_active = delay.is_active
        db_model_obj.delay_rate = delay.delay_rate
        db_model_obj.frequency = delay.frequency

        return db_model_obj

    def map(self):
        pass

@EffectBaseModel.register_effect(ByPass)
class ByPassModel(EffectBaseModel):
    effect_type: str = "ByPass"

    @staticmethod
    def reverse_map(base_object: ByPass) -> 'EffectBaseModel':
        db_model_obj = ByPassModel()

        db_model_obj.effect_type = "ByPass"
        db_model_obj.volume = base_object.volume
        db_model_obj.is_active = base_object.is_active

        return db_model_obj

    def map(self):
        pass

