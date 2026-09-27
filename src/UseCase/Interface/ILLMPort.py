from abc import ABC, abstractmethod

class ILLMPort(ABC):

    @abstractmethod
    def query(self, form_info):
        raise NotImplementedError
