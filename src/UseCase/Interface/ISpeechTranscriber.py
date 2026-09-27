from abc import ABC, abstractmethod

class ISpeechTranscriber(ABC):

    @abstractmethod
    def transcribe(self, audio) -> str:
        raise NotImplementedError
