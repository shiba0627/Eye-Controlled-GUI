import tkinter as tk
from PIL import Image, ImageTk
from config.filepath import CW, CW_ACTIVE, CW_ATTENTION, CW_LOCK
from config.filepath import CCW, CCW_ACTIVE, CCW_ATTENTION, CW_LOCK
from config.filepath import BUTTONS
from config.static import BUTTON_SIZE_RATIO
from typing import TypedDict

class BaseButton:
    def __init__(self, canvas, name = None, area = None, cmd = None):
        self.name = name#ボタンの種類
        self.canvas = canvas
        width = int(area[2] - area[0])
        height = int(area[3] - area[1])
        self.img = ImageTk.PhotoImage(Image.open(BUTTONS[self.name]['normal']).resize((width, height)))

        print(BUTTONS['forward']['normal'])

class GUIapp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('zoomed')#ウィンドウ最大化
        self.root.update_idletasks()#ウィンドウ表示待ち

        # ウィンドウサイズを取得
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

        self.canvas = tk.Canvas(self.root, width = self.width, height = self.height)
        self.canvas.pack(fill='both', expand=True)

        button_list = [
            ('forward', 1/2, 1/6, 'w'),
            ('ccw', 1/4, 1/2, 'a'),
            ('cw', 3/4, 1/2, 'd'),
            ('stop', 1/2, 1/2, 's'),
            ('back', 1/2, 5/6, 'z')
        ]

        self.buttons = []#各ボタンのオブジェクトを格納するリスト
        for name, center_x_ratio, center_y_ratio, cmd in button_list:
            center_x = center_x_ratio * self.width
            center_y = center_y_ratio * self.height
            area = self._calc_area(center_x, center_y)
        print(f'width = {self.width}, height = {self.height}')
    
    def _calc_area(self, center_x, center_y):
        button_size = BUTTON_SIZE_RATIO * self.width
        area = (center_x - button_size/2,
                center_y - button_size/2,
                center_x + button_size/2,
                center_y + button_size/2)
        return area
        


def main():
    app = GUIapp()

if __name__ == '__main__':
    main()
