from dataclasses import dataclass, field

@dataclass
class FormInfo:
    image_path           : str = ''
    image_no             : str = ''
    original             : str = ''
    grammar_corrected    : str = ''
    grammar_explanation  : str = ''
    meaning_corrected    : str = ''
    meaning_pronunciation: str = ''
    meaning_explanation  : str = ''
    other                : str = ''
    
    def update_from_dict(self, data: dict):
        for key, value in data.items():
            if(hasattr(self, key)):
                setattr(self, key, value)
               