from abc import abstractmethod

from pydantic import BaseModel

from models.effects.EffectBase import Effect


class EffectDto(BaseModel):
    volume: int
    is_active: bool
    audio_in: any
    audio_out: any

    @abstractmethod
    def map(self) -> Effect:
        pass