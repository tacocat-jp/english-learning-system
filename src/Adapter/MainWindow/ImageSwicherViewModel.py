from pathlib import Path

from src.Common.config import get_config
from src.Common.Constant import IMAGE_PATH

class ImageSwicherViewModel:
    
    def __init__(self):
        self.image_path_list = self.__get_files_with_extensions()
        self.display_image_no = 0
        
    def __get_files_with_extensions(self):
        
        path = Path(IMAGE_PATH)
        image_path_list = []
        
        extensions_list = self.__target_extensions()
        
        for ext in extensions_list:
            image_path_list.extend([str(p) for p in path.glob(f"*{ext}")])

        return image_path_list
    
    def __target_extensions(self):
        """ 読み込み対象の拡張子を取得する """
        extensions = get_config('Image', 'extensions').split(',')
        extensions_list = [
            ext.strip() for ext in extensions
            ]
        
        return extensions_list
    
    def get_image_num(self):
        return len(self.image_path_list)
    
    def get_previous_image_path(self):
        """ 前の画像のパスを返す。 """
        self.display_image_no -= 1
        if(self.display_image_no < 0):
            self.display_image_no = len(self.image_path_list) - 1
            
        return self.display_image_no, self.image_path_list[self.display_image_no]
       
    def get_next_image_path(self):
        """ 次の画像のパスを返す。 """
        self.display_image_no += 1
        if(len(self.image_path_list) <= self.display_image_no):
            self.display_image_no = 0
            
        return self.display_image_no, self.image_path_list[self.display_image_no]
    
    def get_current_image_path(self):
        """ 現在表示している画像のパスを返す。 """
        return self.image_path_list[self.display_image_no]
    
    def get_selected_image_path(self, image_no):
        """ 指定された画像のパスを返す。 """
        self.display_image_no = image_no - 1
        return self.image_path_list[self.display_image_no]
    