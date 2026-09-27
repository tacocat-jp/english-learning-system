from abc import ABC, abstractmethod

class IFormInput(ABC):

    @abstractmethod
    def get_form_info(self):
        raise NotImplementedError
    