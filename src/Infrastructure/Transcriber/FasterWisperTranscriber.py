import numpy as np
from faster_whisper import WhisperModel

from src.Common.config import get_config
from src.UseCase.Interface.ISpeechTranscriber import ISpeechTranscriber

class FasterWisperTranscriber(ISpeechTranscriber):
    
    def transcribe(self, audio: 'np.ndarray') -> str:
        """ 音声からテキストを生成する。 """
        size = get_config('SpeechTranscriber', 'faster_wisper_size')

        model = WhisperModel(
            size,
            compute_type="int8"
            )
        
        # (n, 1)を(n,)に変換する。model.transcribe()は一次元のデータしか受け付けないため。
        audio = np.concatenate(audio).squeeze()
        segments, _ = model.transcribe(audio, language='en')
        text = self.__build_english_text(segments)
        
        return text
        
    def __build_english_text(self, segments):
        """ 文字起こし結果のセグメントから英文を生成する。 """
        
        text = "".join(segment.text for segment in segments)
        
        # 英文生成直後は" This is a pen"のような英文が生成される。
        # 先頭の半角空白の削除、文末のピリオドを補完して整形する。
        text = text.lstrip()
        
        if(text == ''):
            return ''
        
        if not text.endswith(('.', '?', '!')):
            text += '.'
            
        return text
    