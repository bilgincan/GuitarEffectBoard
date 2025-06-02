from multiprocessing.spawn import freeze_support

from models.audio_device.audio_in.Microphone import Microphone
from models.audio_device.audio_out.Speaker import Speaker
from models.effect_board.EffectBoardBase import EffectBoard
import soundcard as sc

class ConcretePedalBoard:
    microphone_device = sc.default_microphone()
    speaker_device = sc.default_speaker()

    audio_in = Microphone(microphone=microphone_device)
    # audio_in = SampleAudioGenerator()
    audio_out = Speaker(speaker=speaker_device)

    effect_board: EffectBoard



