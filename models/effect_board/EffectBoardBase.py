from abc import ABC

from exception.NoPositionFoundException import NoPositionFound
from exception.OutOfBound import OutOfBoundException
from models.effects.EffectBase import Effect

class EffectBoard(ABC):
    board_size: int # this size indicates how many effect pedals the board can carry
    effects: list

    def __init__(self, board_size: int) -> None:
        self.board_size = board_size
        self.effects = [None] * board_size

    def add_effect(self, position: int, effect: Effect):
        if position >= self.board_size:
            raise OutOfBoundException(position)

        if self.effects[position] is None:
            self.effects.insert(position, effect)
        else:
            raise NoPositionFound(position)

    def remove_effect(self, position: int):
        if position >= self.board_size:
            raise OutOfBoundException(position)

        self.effects.insert(position, None)

    def clear_board(self):
        self.effects = [None] * self.board_size
