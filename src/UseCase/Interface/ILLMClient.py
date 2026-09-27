from abc import ABC, abstractmethod

class ILLMClient(ABC):

    @abstractmethod
    def generate(self, text: str) -> str:
        raise NotImplementedError
