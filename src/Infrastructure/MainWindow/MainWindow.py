import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from src.Common.config import *

from src.Common.Constant import *
from src.Adapter.UpdateController.Interface.IFormInput import IFormInput

class MainWindow(IFormInput):
    
    def __init__(self, image_switcher):
        self.image_switcher = image_switcher
        self.english_learning_system = None
    
    def dependency_injection(self, english_learning_system):
        self.english_learning_system = english_learning_system
        
    def create_frame(self):
        self.root = tk.Tk()

        width, height = getint_config('Window', 'width'), getint_config('Window', 'height')
        self.root.geometry(f"{width}x{height}")

        self.frame = {
            'select_image'         : ttk.Frame(self.root),
            'image'                : ttk.Frame(self.root),
            'original_button'      : ttk.Frame(self.root),
            'original'             : ttk.Frame(self.root),
            'grammar_button'       : ttk.Frame(self.root),
            'grammar_corrected'    : ttk.Frame(self.root),
            'grammar_explanation'  : ttk.Frame(self.root),
            'meaning_button'       : ttk.Frame(self.root),
            'meaning_pronunciation': ttk.Frame(self.root),
            'meaning_corrected'    : ttk.Frame(self.root),
            'meaning_explanation'  : ttk.Frame(self.root),
            'alternative_button'   : ttk.Frame(self.root),
            'other'                : ttk.Frame(self.root),
        }

        self.root.grid_columnconfigure(0, weight=1)
        self.frame['select_image'].grid_columnconfigure(0, weight=1)
        self.frame['select_image'].grid_columnconfigure(6, weight=1)
        self.frame['original'].grid_columnconfigure(0, weight=1)
        self.frame['grammar_corrected'].grid_columnconfigure(0, weight=1)
        self.frame['grammar_explanation'].grid_columnconfigure(0, weight=1)
        self.frame['meaning_corrected'].grid_columnconfigure(0, weight=1)
        self.frame['meaning_pronunciation'].grid_columnconfigure(0, weight=1)
        self.frame['meaning_explanation'].grid_columnconfigure(0, weight=1)
        self.frame['other'].grid_columnconfigure(0, weight=1)
                
        self.frame['select_image'].grid(row=0, column=0, sticky='ew')
        self.frame['image'].grid(row=1, column=0, sticky='ew')
        self.frame['original_button'].grid(row=2, column=0, sticky='w')
        self.frame['original'].grid(row=3, column=0, sticky='ew')
        self.frame['grammar_button'].grid(row=4, column=0, sticky='w')
        self.frame['grammar_corrected'].grid(row=5, column=0, sticky='ew')
        self.frame['grammar_explanation'].grid(row=6, column=0, sticky='ew')
        self.frame['meaning_button'].grid(row=7, column=0, sticky='w')
        self.frame['meaning_corrected'].grid(row=8, column=0, sticky='ew')
        self.frame['meaning_pronunciation'].grid(row=9, column=0, sticky='ew')
        self.frame['meaning_explanation'].grid(row=10, column=0, sticky='ew')
        self.frame['alternative_button'].grid(row=11, column=0, sticky='w')
        self.frame['other'].grid(row=12, column=0, sticky='ew')
        
        # 画像表示フレームは大きさを固定させる。
        self.image_size = (
            getint_config('Image', 'width'),
            getint_config('Image', 'height')
            )
        self.frame['image'].configure(width=self.image_size[0], height=self.image_size[1])
        self.frame['image'].grid_propagate(False)
        
        ### 値取得、設定用の変数
        # tk.Label用
        self.state_label = None
        # tk.Entry用
        self.image_no_var = tk.IntVar(value=1)
        # tk.Text用
        # textvariableのオプションが存在しないため
        # ウィジェットのオブジェクトから値の取得、設定を行う。
        self.widget = {}
        
        # スコープを抜けても画像データが消えないように
        # インスタンス変数として保持し続ける必要がある。
        self.image = None       

        self.__create(self.frame)
        
    def __create(self, frame):
        # 画像選択フレーム
        tk.Label(frame['select_image'], text='画像：').grid(row=0, column=0, sticky='e')
        ttk.Entry(frame['select_image'], textvariable=self.image_no_var, width=10, justify='center').grid(row=0, column=1)
        image_num = self.image_switcher.get_image_num()
        tk.Label(frame['select_image'], text=f'　/　{image_num}　', justify='right').grid(row=0, column=2)
        tk.Button(frame['select_image'], text='移動', command=self.move_button_click, width=10).grid(row=0, column=3)
        
        tk.Button(frame['select_image'], text='戻る', command=self.back_button_click, width=10).grid(row=0, column=4)
        tk.Button(frame['select_image'], text='次へ', command=self.next_button_click, width=10).grid(row=0, column=5)

        # 画像フレーム
        self.image_label = tk.Label(frame['image'])
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")
        path = self.image_switcher.get_selected_image_path(1)       # 先頭（１番目）の画像データを表示する。
        self.__set_image(path)
       
        ### ユーザー入力
        # ボタン欄
        tk.Label(frame['original_button'], text='①ユーザー入力：', height=2).grid(row=0, column=0)
        tk.Button(frame['original_button'], text='一括チェック開始\n（①→②→③へ出力）', command=self.run_all_button_click).grid(row=0, column=1)
        tk.Button(frame['original_button'], text='発音', height=2, command=self.original_pronounce_button_click).grid(row=0, column=2)
        tk.Label(frame['original_button'], text='', width=5).grid(row=0, column=3)
        self.state_label = tk.Label(frame['original_button'], text='状態 ⇒ 【待機中】', height=2)
        self.state_label.grid(row=0, column=4)
        tk.Button(frame['original_button'], text='録音', height=2, command=self.record_start_button_click).grid(row=0, column=5)
        tk.Button(frame['original_button'], text='停止', height=2, command=self.record_stop_button_click).grid(row=0, column=6)
        tk.Button(frame['original_button'], text='中止', height=2, command=self.record_cancel_button_click).grid(row=0, column=7)

        # 入力テキスト
        self.widget['original'] = tk.Text(frame['original'], height=2)
        self.widget['original'].grid(row=0, column=0, sticky='ew')
        
        ### 文法チェック
        # ボタン欄
        tk.Label(frame['grammar_button'], text='②文法チェック：', height=2).grid(row=0, column=0)
        tk.Button(frame['grammar_button'], text='チェック開始\n（①→②へ出力）', command=self.grammar_check_button_click).grid(row=0, column=1)
        tk.Button(frame['grammar_button'], text='発音', height=2, command=self.grammar_pronounce_button_click).grid(row=0, column=2)
        
        # 修正テキスト
        self.widget['grammar_corrected'] = tk.Text(frame['grammar_corrected'], height=2)
        self.widget['grammar_corrected'].grid(row=0, column=0, sticky='ew')
        
        # 解説テキスト
        self.widget['grammar_explanation'] = tk.Text(frame['grammar_explanation'], height=5)
        self.widget['grammar_explanation'].grid(row=0, column=0, sticky='ew')
        
        ### 意味チェック
        # ボタン欄
        tk.Label(frame['meaning_button'], text='③意味チェック：', height=2).grid(row=0, column=0)
        tk.Button(frame['meaning_button'], text='チェック開始\n（②→③へ出力）', command=self.meaning_check_button_click).grid(row=0, column=1)
        tk.Button(frame['meaning_button'], text='発音', height=2, command=self.meaning_pronounce_button_click).grid(row=0, column=2)
                
        # 修正テキスト
        self.widget['meaning_corrected'] = tk.Text(frame['meaning_corrected'], height=2)
        self.widget['meaning_corrected'].grid(row=0, column=0, sticky='ew')

        # 発音記号テキスト
        font_ = (get_config('Font', 'pronunciation'), 10)
        self.widget['meaning_pronunciation'] = tk.Text(frame['meaning_pronunciation'], font=font_, height=2)
        self.widget['meaning_pronunciation'].grid(row=0, column=0, sticky='ew')
        
        # 解説テキスト
        self.widget['meaning_explanation'] = tk.Text(frame['meaning_explanation'], height=5)
        self.widget['meaning_explanation'].grid(row=0, column=0, sticky='ew')
        
        # その多
        tk.Label(frame['alternative_button'], text='その他機能：', height=2).grid(row=0, column=0)
        tk.Button(frame['alternative_button'], text='③の別解生成', height=2, command=self.alternative_generate_button_click).grid(row=0, column=1)
        
        # その他テキスト
        self.widget['other'] = tk.Text(frame['other'], height=7)
        self.widget['other'].grid(row=0, column=0, sticky='ew')

    def loop(self):
        self.root.mainloop()
        
    def move_button_click(self):
        """ 移動ボタン押下時の動作"""
        path = self.image_switcher.get_selected_image_path(self.image_no_var.get())
        self.__set_image(path)
        
    def back_button_click(self):
        """ 戻るボタン押下時の動作"""
        image_no, path = self.image_switcher.get_previous_image_path()
        self.image_no_var.set(image_no + 1)
        self.__set_image(path)        
        
    def next_button_click(self):
        """ 次へボタン押下時の動作"""
        image_no, path = self.image_switcher.get_next_image_path()
        self.image_no_var.set(image_no + 1)
        self.__set_image(path)
        
    def __set_image(self, path):
        """ 画像表示用フレームにその大きさを超えない範囲で拡大し表示する。縦横比は維持する。"""
        original_image = Image.open(path)
        original_image.thumbnail(self.image_size,Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(original_image)
        self.image_label.config(image=self.image)
        
    def record_start_button_click(self):
        """ 録音ボタン押下時の動作 """
        self.english_learning_system.record_start()

    def record_stop_button_click(self):
        """ 停止ボタン押下時の動作 """
        self.english_learning_system.record_stop()
        
    def record_cancel_button_click(self):
        """ 取り消しボタン押下時の動作 """
        self.english_learning_system.record_cancel()
                
    def run_all_button_click(self):
        """ すべてチェック開始ボタン押下時の動作 """
        self.english_learning_system.run_all()
    
    def original_pronounce_button_click(self):
        """ ユーザー入力テキストの発音ボタン押下時の動作 """
        self.english_learning_system.pronounce(self.widget['original'].get('1.0','end-1c'))
        
    def grammar_check_button_click(self):
        """ 文法のチェック開始ボタン押下時の動作 """
        self.english_learning_system.grammar_check()
        
    def grammar_pronounce_button_click(self):
        """ 文法チェックの発音ボタン押下時の動作 """
        self.english_learning_system.pronounce(self.widget['grammar_corrected'].get('1.0','end-1c'))
        
    def meaning_check_button_click(self):
        """ 意味のチェック開始ボタン押下時の動作 """
        self.english_learning_system.meaning_check()
        
    def meaning_pronounce_button_click(self):
        """ 意味チェックの発音ボタン押下時の動作 """
        self.english_learning_system.pronounce(self.widget['meaning_corrected'].get('1.0','end-1c'))
        
    def alternative_generate_button_click(self):
        """ 別解の生成ボタン押下時の動作 """
        self.english_learning_system.alternative_generate()
                
    def get_form_info(self):
        """ UIのデータを取得 """
        input_data = {
            'image_no'             : self.image_no_var.get(),
            'image_path'           : self.image_switcher.get_current_image_path(),
            'original'             : self.widget['original'].get('1.0','end-1c'),
            'grammar_corrected'    : self.widget['grammar_corrected'].get('1.0','end-1c'),
            'grammar_explanation'  : self.widget['grammar_explanation'].get('1.0','end-1c'),
            'meaning_corrected'    : self.widget['meaning_corrected'].get('1.0','end-1c'),
            'meaning_pronunciation': self.widget['meaning_pronunciation'].get('1.0','end-1c'),
            'meaning_explanation'  : self.widget['meaning_explanation'].get('1.0','end-1c'),
            'other'                : self.widget['other'].get('1.0','end-1c')
        }
        
        return input_data
                
    def set_form_info(self, set_info):
        """ UI上のtk.Textウィジェットにテキストを表示する。 """
        def set_to_widget(key, value):
            if key in self.widget:
                self.widget[key].delete('1.0', 'end')
                self.widget[key].insert('1.0', value)

        for key, value in set_info.items():
            set_to_widget(key, value)
            
    def set_state(self, state): 
        """ UI上の録音状態ラベルの表記を設定する 。"""
        self.state_label.configure(text=f'状態 ⇒ 【{state}】')
        