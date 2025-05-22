from models.effect_board.EffectBoardBase import EffectBoard
from models.effects.Delay import Delay

delay = Delay()
pedal_board = EffectBoard(board_size=2)

pedal_board.add_effect(0, delay)
pedal_board.activate_pedal(0)

