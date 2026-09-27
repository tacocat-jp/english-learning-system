from abc import ABC, abstractmethod

class ITextToSpeech(ABC):

    @abstractmethod
    def synthesize(self, test: str) -> 'audio':
        raise NotImplementedError
