from models.effect_board.EffectBoardBase import EffectBoard


class User:
    name: str
    id: str
    effect_board: EffectBoard

    def __init__(self, id: str, name: str, effect_board: EffectBoard):
        self.name = name
        self.id = id
        self.effect_board = effect_board