from abc import ABC
from threading import Thread

from exception.NoPedalFoundException import NoPedalFound
from exception.NoPositionFoundException import NoPositionFound
from exception.OutOfBound import OutOfBoundException
from models.effects.EffectBase import Effect

class EffectBoard(ABC):
    id: str
    board_size: int # this size indicates how many effect pedals the board can carry
    effects: list[Effect]
    effect_channel_threads: list[Thread]

    def __init__(self, board_size: int) -> None:
        self.board_size = board_size
        self.effects = [None] * board_size
        self.effect_channel_threads = [None] * board_size

    def add_effect(self, position: int, effect: Effect):
        if position >= self.board_size:
            raise OutOfBoundException(position)

        if self.effects[position] is None:
            self.effects[position] = effect
        else:
            raise NoPositionFound(position)

    def remove_effect(self, position: int):
        if position >= self.board_size:
            raise OutOfBoundException(position)

        self.effects[position] = None

    def get_effect(self, position: int) -> Effect:
        if position >= self.board_size:
            raise OutOfBoundException(position)

        effect: Effect = self.effects[position]

        if effect is None:
            raise NoPedalFound(position)

        return effect

    def clear_board(self):
        self.effects = [None] * self.board_size

    def activate_pedal(self, position: int) -> None:
        if position >= self.board_size:
            raise OutOfBoundException(position)

        if self.effects[position] is None:
            raise NoPedalFound(position)

        pedal: Effect = self.effects[position]

        pedal_thread = Thread(target=pedal.activate_effect)
        pedal_thread.start()
        self.effect_channel_threads.insert(position, pedal_thread)

    def deactivate_pedal(self, position: int) -> None:
        if position >= self.board_size:
            raise OutOfBoundException(position)

        if self.effect_channel_threads[position] is None:
            raise NoPedalFound(position)

        pedal: Effect = self.effects[position]
        pedal_thread: Thread = self.effect_channel_threads[position]

        pedal.deactivate_effect()
        if pedal_thread.is_alive():
            pedal_thread.join(timeout=0.5)
