from src.Common.config import get_config
from src.UseCase.Interface.ILLMPort import ILLMPort

class GrammarCorrectedLLMPort(ILLMPort):
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def query(self, form_info):
        """ 文法の修正をAIモデルに依頼する。 """
        messages = self.__create_messages(form_info)
    
        try:
            response = self.llm_client.generate(messages)
            answer = response.message.content

            return {'grammar_corrected': answer}
        
        except:
            return {'grammar_corrected': '生成失敗'}
    
    def __create_messages(self, form_info):
        """ LLMに渡すmessagesを作成する。 """
        original = f"English Text: {form_info.original}"
        prompt = get_config('Grammar', 'correct_prompt')
        
        messages=[
            {
                "role"   : "user",
                "content": prompt + '\n' + original,
            }
        ]
        
        return messages
    