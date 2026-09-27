import numpy as np
import sounddevice as sd

from src.Common.Constant import *
from src.UseCase.Interface.IRecorder import IRecorder

class SoundDeviceRecorder(IRecorder):
    
    def __init__(self):
        self.stream = None
        self.audio = []

    def start(self):
        def _callback(indata, frames, time, status):
            """ 
            マイクからサンプリングデータが届くたびに呼ばれる。
                indata: その時点で取得された音声データ。
                frames: サンプル数。
                time  : 音声データの取得時刻を表す情報
                status: 録音中に何か問題や状態変化が発生したかの情報。
            """
            self.audio.append(indata.copy())
        
        self.audio = []

        self.stream = sd.InputStream(
            samplerate=SAMPLERATE,
            channels=1,
            callback=_callback
        )
        self.stream.start()

    def stop(self) -> 'np.ndarray':
        self.stream.stop()
        self.stream.close()
        self.stream = None
        
        audio = self.audio.copy()
        audio = np.concatenate(audio, axis=0)
        self.audio = []
        
        return audio

    def cancel(self) -> 'np.ndarray':
        self.stream.stop()
        self.stream.close()
        self.stream = None
        self.audio = []
        