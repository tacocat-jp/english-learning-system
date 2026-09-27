from src.Common.config import get_config
from src.UseCase.Interface.ILLMPort import ILLMPort

class GrammarExplanationLLMPort(ILLMPort):
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def query(self, form_info):
        """ 文法の説明をAIモデルに依頼する。 """
        
        if(form_info.original == form_info.grammar_corrected):
            return {'grammar_explanation': '正しい英文です。'}
        
        messages = self.__create_messages(form_info)

        try:
            response = self.llm_client.generate(messages)
            answer = response.message.content
            
            return {'grammar_explanation': answer}
        
        except:
            return {'grammar_explanation': '生成失敗'}
    
    def __create_messages(self, form_info):
        """ LLMに渡すmessagesを作成する。 """
        original = f"Original English Text: {form_info.original}"
        grammar_corrected = f"Corrected English Text: {form_info.grammar_corrected}"
                
        prompt = get_config('Grammar', 'explanation_prompt')
        
        messages=[
            {
                "role"   : "user",
                "content": prompt + '\n' + original + '\n' + grammar_corrected,
            }
        ]
        
        return messages