import os
import tkinter as tk
from PIL import Image, ImageTk
import time
from enum import Enum

HOVER_TIME = 0.5
BUTTON_SIZE_RATIO = 0.16#ボタンサイズ 画面横幅の何倍か
ARC_RADIUS = 30

# ===画像パス===
# 絶対パスに変換
IMG_DIR = './img'
if not os.path.isabs(IMG_DIR):#相対パスなら
    IMG_DIR = os.path.abspath(IMG_DIR)#絶対パスに変換
FORWARD, BACK, CW, CCW, STOP = [os.path.join(IMG_DIR, name) for name in 
                                ['forward.png', 'back.png', 'cw.png', 'ccw.png', 'stop.png']]
FORWARD_ACTIVE, BACK_ACTIVE, CW_ACTIVE, CCW_ACTIVE, STOP_ACTIVE = [p.replace('.png', '_active.png') for p in [FORWARD, BACK, CW, CCW, STOP]]
FORWARD_ATTENTION, BACK_ATTENTION, CW_ATTENTION, CCW_ATTENTION, STOP_ATTENTION = [p.replace('.png', '_attention.png') for p in [FORWARD, BACK, CW, CCW, STOP]]
FORWARD_LOCK, BACK_LOCK, CW_LOCK, CCW_LOCK, STOP_LOCK = [p.replace('.png', '_lock.png') for p in [FORWARD, BACK, CW, CCW, STOP]]

class ImageCache:#画像をメモリに保持しておく
    cache={}
    @classmethod#クラスメソッド インスタンスを作らなくても呼べる
    def load(cls, path, size):
        key = (path, size)#辞書のキー
        if key not in cls.cache:#まだキャッシュに画像が無いとき
            img = Image.open(path).resize(size)
            cls.cache[key] = ImageTk.PhotoImage(img)#キャッシュに保存
        return cls.cache[key]

class FrameName(str, Enum):
    SETTINGS = 'settings'
    CONTROL = 'control'

class BaseFrame(tk.Frame):
    def __init__(self, master = None, chage_page_callback = None):
        super().__init__(master)
        # Frameを画面ウィンドウいっぱいに敷く
        self.pack(fill=tk.BOTH, expand=True)#Frameをウィンドウ(master)いっぱいに配置
        self.config(bg="red")

        #画面サイズを取得
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        self.change_page = chage_page_callback#フレーム遷移のコールバック
        self.canvas = tk.Canvas(self, width = self.width, height = self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)#canvasをmasterいっぱいに配置
        #tk.Button(self, text = "back", command = lambda: self.change_page(FrameName.CONTROL), font=("Arial", 16)).pack()
        self.buttons = []
    def _calc_area(self, center_x_ratio, center_y_ratio):
        button_size_half = (BUTTON_SIZE_RATIO * self.width) / 2
        min_x = center_x_ratio * self.width - button_size_half
        max_x = center_x_ratio * self.width + button_size_half
        min_y = center_y_ratio * self.height - button_size_half
        max_y = center_y_ratio * self.height + button_size_half
        return (min_x, min_y, max_x, max_y)
    
    def check_cursor(self):
        x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        y = self.master.winfo_pointery() - self.master.winfo_rooty()

        #各ボタンにマウス位置を通知
        for button in self.buttons:
            now_cmd = button.update(x,y)


class SettingFrame(tk.Frame):
    def __init__(self, master = None, chage_page_callback = None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg="lightblue")
        self.change_page = chage_page_callback

class ControlButton:# ボタンのベースクラス
    def __init__(self, canvas, img_path, active_path, lock_path, attention_path, area, cmd):
        self.canvas = canvas
        width = int(area[2] - area[0])
        height = int(area[3] - area[1])
        self.img = ImageCache.load(img_path, (width, height))
        self.img_lock = ImageCache.load(lock_path, (width, height))
        self.img_active = ImageCache.load(active_path, (width, height))
        self.img_attention = ImageCache.load(attention_path, (width, height))
        self.area = area
        self.stay_time = HOVER_TIME
        self.enter_time = None
        self.arc_id = None
        self.arc_radius = ARC_RADIUS
        self.cmd = cmd
        self.image_id = self.canvas.create_image(area[0], area[1], image=self.img, anchor="nw")
        self.active = False
    def draw_arc(self, x, y, percent):
        pass
    def set_attention(self):
        #ボタンをattentionにする
        self.canvas.itemconfig(self.image_id, image=self.img_attention)
    def set_nomal(self):
        #ボタンをnomalにする
        self.canvas.itemconfig(self.image_id, image=self.img)
    def set_active(self):
        #ボタンをactiveにする
        self.enter_time = None
        self.active = True
        if self.arc_id:
            self.canvas.delete(self.arc_id)
            self.arc_id = None
        self.canvas.itemconfig(self.image_id, image=self.img_active)
    def update(self, cursor_x, cursor_y):#カーソルのxy座標を受け取る
        if self.active:#Trueなら、何もしない
            return None
        x1, y1, x2, y2 = self.area
        if x1 <= cursor_x <= x2 and y1 <= cursor_y <= y2:
            if self.enter_time is None:
                self.enter_time = time.time()
            elapsed = time.time = self.enter_time
            percent = min(elapsed / self.stay_time * 100, 100)
            self.draw_arc(cursor_x + 40, cursor_y + 40, percent)
            if elapsed >= self.stay_time:
                print(f'{self.cmd}')
                self.set_active()
                return self.cmd
            else:
                self.set_attention()
        else:
            self.set_nomal()
        return None

class ControlFrame(BaseFrame):# 操作画面
    def __init__(self, master = None, chage_page_callback = None):
        super().__init__(master,  chage_page_callback)
        button_list = [
            (FORWARD, FORWARD_ACTIVE, FORWARD_LOCK, FORWARD_ATTENTION, 2/4, 1/6, 'w'),
            (CCW, CCW_ACTIVE, CCW_LOCK, CCW_ATTENTION, 1/4, 3/6, 'a'),
            (CW, CW_ACTIVE, CW_LOCK, CW_ATTENTION, 3/4, 3/6, 'd'),
            (STOP, STOP_ACTIVE, STOP_LOCK, STOP_ATTENTION, 2/4, 3/6, 's'),
            (BACK, BACK_ACTIVE, BACK_LOCK, BACK_ATTENTION, 2/4, 5/6, 'z'),
        ]
        
        for img, active, lock, attention, center_x_ratio, center_y_ratio, cmd in button_list:
            area = self._calc_area(center_x_ratio,center_y_ratio)
            self.buttons.append(ControlButton(self.canvas, img, active, lock, attention,area, cmd))

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('eye controll')
        self.root.state("zoomed")
        self.current_frame = None#現在表示中のフレーム
        self.show_frame(FrameName.CONTROL)

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
        if frame_name == FrameName.CONTROL:
            self.current_frame = ControlFrame(self.root, self.show_frame)
        elif frame_name == FrameName.SETTINGS:
            self.current_frame = SettingFrame(self.root, self.show_frame)
    def run(self):
        self.root.mainloop()

def main():
    app = App()
    app.run()

if __name__ == '__main__':
    main()