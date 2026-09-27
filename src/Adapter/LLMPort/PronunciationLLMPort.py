from src.Common.config import get_config
from src.UseCase.Interface.ILLMPort import ILLMPort

class PronunciationLLMPort(ILLMPort):
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def query(self, form_info):
        """ 意味のチェックをAIモデルに依頼する。 """
        messages = self.__create_messages(form_info)
        
        try:
            response = self.llm_client.generate(messages)
            text = response.message.content
            
            return {'meaning_pronunciation': text}
        
        except:
            return {'meaning_pronunciation': '生成失敗'}
        
    def __create_messages(self, form_info):
        """ LLMに渡すmessagesを作成する。 """
        meaning_corrected = 'English text:' + form_info.meaning_corrected
        
        prompt = get_config('Pronunciation', 'prompt')
        
        messages=[
            {
                "role"   : "user",
                "content": prompt + '\n' + meaning_corrected,
            }
        ]
        return messages
