class EnglishLearningSystem:
    """
    各機能を実行するときの入り口となるクラス。
    処理の前にUIに入力された値を一時変数form_infoに取得し、
    処理が終わったら最新のform_infoをUIに戻す方針でメソッドを実装する。
    """
    
    def __init__(self, gateways):
        """
        引数：
            gateways: 本クラスが依存するオブジェクトを保持する辞書
        """
        self.gateways = gateways
        
        # 現在の状態（idle: 待機中、 recording: 録音中）
        self.state = 'idle'     
        
    def record_start(self):
        if(self.state=='recording'):
            return
        
        self.gateways['recorder'].start()
        self.state = 'recording'
        self.gateways['update_controller'].set_state(self.state)
        
    def record_stop(self):
        if(self.state =='idle'):
            return
        
        form_info =  self.gateways['update_controller'].get_form_input()
        
        audio = self.gateways['recorder'].stop()
        
        form_info.original = self.gateways['speech_transcriber'].transcribe(audio)
        self.gateways['update_controller'].set_form_info(form_info)
        
        self.state = 'idle'
        self.gateways['update_controller'].set_state(self.state)

    def record_cancel(self):
        if(self.state=='idle'):
            return
        
        self.gateways['recorder'].cancel()
        self.state = 'idle'
        self.gateways['update_controller'].set_state(self.state)

    def run_all(self):
        self.grammar_check()
        self.meaning_check()
        
    def grammar_check(self):
        if(self.state=='recording'):
            self.record_cancel()
            
        form_info =  self.gateways['update_controller'].get_form_input()
        
        if(form_info.original == ''):
            return
        
        dic_answer = self.gateways['grammar_corrected'].query(form_info)
        form_info.update_from_dict(dic_answer)
        
        dic_answer = self.gateways['grammar_explanation'].query(form_info)
        form_info.update_from_dict(dic_answer)
        
        self.gateways['update_controller'].set_form_info(form_info)
        
    def meaning_check(self):
        if(self.state=='recording'):
            self.record_cancel()
            
        form_info =  self.gateways['update_controller'].get_form_input()
        
        if(form_info.grammar_corrected == ''):
            return
        
        dic_answer = self.gateways['meaning_corrected'].query(form_info)
        form_info.update_from_dict(dic_answer)
        
        dic_answer = self.gateways['meaning_explanation'].query(form_info)
        form_info.update_from_dict(dic_answer)

        dic_answer = self.gateways['pronunciation'].query(form_info)
        form_info.update_from_dict(dic_answer)
                
        self.gateways['update_controller'].set_form_info(form_info)
        
    def alternative_generate(self):
        if(self.state=='recording'):
            self.record_cancel()
            
        form_info =  self.gateways['update_controller'].get_form_input()
        
        if(form_info.meaning_corrected == ''):
            return
        
        dic_answer = self.gateways['alternative_answer'].query(form_info)
        form_info.update_from_dict(dic_answer)
        
        self.gateways['update_controller'].set_form_info(form_info)
        
    def pronounce(self, text):
        if(self.state=='recording'):
            self.record_cancel()
        if(text == ''):
            return
        
        audio = self.gateways['text_to_speech'].synthesize(text)
        self.gateways['player'].play(audio)
        