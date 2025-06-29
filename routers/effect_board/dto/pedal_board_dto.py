from pydantic import BaseModel

from routers.effects.dto.effect_dto import EffectDto


class PedalBoardInputDto(BaseModel):
    board_size: int

class PedalBoardOutputDto(BaseModel):
    board_id: str
    board_size: int
    effects: list[EffectDto]

class EffectInBoardDto(BaseModel):
    position: int
    effect: EffectDto
    board_id: str

class EffectBoardUserDto(BaseModel):
    id: str
    user_id: str