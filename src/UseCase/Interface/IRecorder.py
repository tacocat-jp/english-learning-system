from abc import ABC, abstractmethod

class IRecorder(ABC):

    @abstractmethod
    def start(self):
        raise NotImplementedError
    
    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def cancel(self):
        raise NotImplementedError
    