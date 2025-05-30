from multiprocessing.spawn import freeze_support

from models.audio_device.audio_in.Microphone import Microphone
from models.audio_device.audio_in.SampleAudioGenerator import SampleAudioGenerator
from models.audio_device.audio_out.Speaker import Speaker
from models.effect_board.EffectBoardBase import EffectBoard
from models.effects.ByPass import ByPass
from models.effects.Delay import Delay
import soundcard as sc

# audio_in: _Microphone = sc.default_microphone(), audio_out: _Speaker = sc.default_speaker()

microphone_device = sc.default_microphone()
speaker_device = sc.default_speaker()

#audio_in = Microphone(microphone=microphone_device)
audio_in = SampleAudioGenerator()
audio_out = Speaker(speaker=speaker_device)

by_pass = ByPass(audio_in=audio_in, audio_out=audio_out)
delay = Delay(audio_in=audio_in, audio_out=audio_out)
pedal_board = EffectBoard(board_size=2)

pedal_board.add_effect(0, by_pass)
pedal_board.add_effect(1, delay)
#delay.deactivate_effect()

if __name__ == '__main__':
    freeze_support()
    pedal_board.activate_pedal(0)
    pedal_board.activate_pedal(1)
    #pedal_board.deactivate_pedal(1)

