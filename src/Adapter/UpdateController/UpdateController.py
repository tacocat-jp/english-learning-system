from dataclasses import asdict

from src.Common.Constant import *
from src.UseCase.Interface.IUpdateController import IUpdateController
from src.UseCase.FormInfo import FormInfo

class UpdateController(IUpdateController):
    """
    UIの入力情報をシステム本体で利用する形式に変換して渡す橋渡し用のクラス。
    """
    def __init__(self, main_window):
        self.main_window = main_window
        
    def get_form_input(self):
        input_data = self.main_window.get_form_info()
        form_info = FormInfo()
        form_info.update_from_dict(input_data)
        
        return form_info
        
    def set_form_info(self, form_info):
        set_info = asdict(form_info)
        
        self.main_window.set_form_info(set_info)
        
    def set_state(self, state):
        if(state=='idle'):
            state_text = '待機中'
        elif(state=='recording'):
            state_text = '録音中'
        else:
            raise ValueError(f"未知のstateが渡されました: {state}")
        
        self.main_window.set_state(state_text)
        