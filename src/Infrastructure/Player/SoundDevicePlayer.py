import numpy as np
import sounddevice as sd

from src.Common.Constant import *
from src.UseCase.Interface.IPlayer import IPlayer

class SoundDevicePlayer(IPlayer):
    
    def play(self, audio: np.ndarray):
        
        # 最大振幅を 1.0に正規化
        # 音声が小さい時に精度が良くなる可能性がある。
        audio = audio / np.max(np.abs(audio))
        
        sd.play(audio, samplerate=SAMPLERATE)
        
        sd.wait()
        