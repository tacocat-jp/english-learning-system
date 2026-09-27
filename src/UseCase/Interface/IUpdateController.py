from abc import ABC, abstractmethod

class IUpdateController(ABC):

    @abstractmethod
    def get_form_input(self):
        raise NotImplementedError
    
    @abstractmethod
    def set_form_info(self, form_info):
        raise NotImplementedError
    
    @abstractmethod
    def set_state(self, state):
        raise NotImplementedError
    