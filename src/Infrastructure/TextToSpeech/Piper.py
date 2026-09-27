import numpy as np
from piper import PiperVoice

from src.Common.Constant import VOICE_PATH
from src.UseCase.Interface.ITextToSpeech import ITextToSpeech

class Piper(ITextToSpeech):

    def synthesize(self, text: str) -> bytes:
        """ テキストをPiperで音声化し、WAV形式の音声データをbytesで返す。 """
        voice = PiperVoice.load(VOICE_PATH + "en_US-lessac-high.onnx")
        
        audio = [
            np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            for chunk in voice.synthesize(text)
        ]

        return np.concatenate(audio)
