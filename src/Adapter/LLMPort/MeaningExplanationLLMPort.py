from src.Common.config import get_config
from src.UseCase.Interface.ILLMPort import ILLMPort

class MeaningExplanationLLMPort(ILLMPort):
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def query(self, form_info):
        """ 意味のチェックをLLMに依頼する。 """
        
        if(form_info.grammar_corrected == form_info.meaning_corrected):
            return {'meaning_explanation': '正しい英文です。'}
       
        messages = self.__create_messages(form_info)
        
        try:
            response = self.llm_client.generate(messages)
            answer = response.message.content
            dic_answer = {
                'meaning_explanation': answer,
            }
            
            return dic_answer
    
        except:
            return{
                'meaning_explanation': '生成失敗',
            }
            
    def __create_messages(self, form_info):
        """ LLMに渡すmessagesを作成する。 """
        grammar_corrected = 'Inaccurate English Text:' + form_info.grammar_corrected
        meaning_corrected = 'Accurate English Text:' + form_info.meaning_corrected
        
        prompt = get_config('Meaning', 'explanation_prompt')
        
        messages=[
            {
                "role"   : "user",
                "content": 
                    prompt + '\n' + grammar_corrected + '\n' + meaning_corrected,
                "images" : [form_info.image_path]
            }
        ]
        
        return messages
    