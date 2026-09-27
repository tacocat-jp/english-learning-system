from abc import ABC, abstractmethod

class IPlayer(ABC):

    @abstractmethod
    def play(self):
        raise NotImplementedError
    