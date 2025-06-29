from repository.effects.EffectBaseModel import EffectBaseModel
from repository.BaseModel import BaseModel
from models.effect_board.EffectBoardBase import EffectBoard
from models.effects.EffectBase import Effect

class EffectBoardModel(BaseModel):
    id: str
    user_id: str
    board_size: int
    effects: list[dict]

    def __init__(self, _id: str, user_id: str, board_size: int, effects: list[EffectBaseModel]):
        self.id = _id
        self.user_id = user_id
        self.board_size = board_size

        self.effects = []
        for effect in effects:
            self.effects.append(effect.__dict__)


    @staticmethod
    def reverse_map(effect_board: EffectBoard):
        return EffectBoardModel(
            _id=effect_board.id,
            user_id=effect_board.user_id,
            board_size=effect_board.board_size,
            effects=EffectBoardModel.transform_effects_into_model(effect_board.effects)
        )


    def map(self):
        pass

    @staticmethod
    def transform_effects_into_model(effects: list[Effect]) -> list[EffectBaseModel]:
        result: list[EffectBaseModel] = []

        for e in effects:
            result.append(EffectBaseModel.reverse_map(e))

        return result



