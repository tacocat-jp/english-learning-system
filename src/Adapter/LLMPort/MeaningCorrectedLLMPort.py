from src.Common.config import get_config
from src.UseCase.Interface.ILLMPort import ILLMPort

class MeaningCorrectedLLMPort(ILLMPort):
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def query(self, form_info):
        """ 意味のチェックをAIモデルに依頼する。 """

        messages = self.__create_messages(form_info)
        
        try:           
            response = self.llm_client.generate(messages)
            answer = response.message.content
            dic_answer = {'meaning_corrected': answer}
            
            return dic_answer
    
        except:
            return{
                'meaning_corrected': '生成失敗'
            }
            
    def __create_messages(self, form_info):
        """ LLMに渡すmessagesを作成する。 """
        grammar_corrected = f"English Text: {form_info.grammar_corrected}"

        prompt = get_config('Meaning', 'correct_prompt')
        
        messages=[
            {
                "role"   : "user",
                "content": prompt + '\n' + grammar_corrected,
                "images" : [form_info.image_path]
            }
        ]
        
        return messages