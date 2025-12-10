import os
import tkinter as tk
from PIL import Image, ImageTk
import time
from enum import Enum

HOVER_TIME = 0.5
BUTTON_SIZE_RATIO = 0.18#ボタンサイズ 画面横幅の何倍か
SETTING_SIZE_RATIO = 0.12
ARC_RADIUS = 30
DEFAULT_SPEED = 5#スピード初期値
MAX_SPEED = 10

# ===画像パス===
# 絶対パスに変換
IMG_DIR = './img'
if not os.path.isabs(IMG_DIR):#相対パスなら
    IMG_DIR = os.path.abspath(IMG_DIR)#絶対パスに変換
FORWARD, BACK, CW, CCW, STOP, SETTING, PLUS, MINUS= [os.path.join(IMG_DIR, name) for name in 
    ['forward.png', 'back.png', 'cw.png', 'ccw.png', 'stop.png', 'setting.png', 'plus.png', 'minus.png']]
FORWARD_ACTIVE, BACK_ACTIVE, CW_ACTIVE, CCW_ACTIVE, STOP_ACTIVE, SETTING_ACTIVE, PLUS_ACTIVE, MINUS_ACTIVE = [p.replace('.png', '_active.png') for p in [FORWARD, BACK, CW, CCW, STOP, SETTING, PLUS, MINUS]]
FORWARD_ATTENTION, BACK_ATTENTION, CW_ATTENTION, CCW_ATTENTION, STOP_ATTENTION, SETTING_ATTENTION, PLUS_ATTENTION, MINUS_ATTENTION = [p.replace('.png', '_attention.png') for p in [FORWARD, BACK, CW, CCW, STOP, SETTING, PLUS, MINUS]]
FORWARD_LOCK, BACK_LOCK, CW_LOCK, CCW_LOCK, STOP_LOCK = [p.replace('.png', '_lock.png') for p in [FORWARD, BACK, CW, CCW, STOP]]

class ImageCache:
    _cache = {}

    @classmethod
    def load(cls, path, size):
        key = (path, size)
        if key in cls._cache:
            return cls._cache[key]

        try:
            img = Image.open(path).resize(size)
        except FileNotFoundError:
            # ロードに失敗したらダミー画像を返す
            img = Image.new("RGB", size, (255, 255, 255))

        tk_img = ImageTk.PhotoImage(img)
        cls._cache[key] = tk_img
        return tk_img

class FrameName(str, Enum):
    SETTINGS = 'settings'
    CONTROL = 'control'

class BaseFrame(tk.Frame):
    def __init__(self, master = None, app_instance = None):
        super().__init__(master)
        # Frameを画面ウィンドウいっぱいに敷く
        self.pack(fill=tk.BOTH, expand=True)#Frameをウィンドウ(master)いっぱいに配置

        #画面サイズを取得
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        self.app = app_instance#フレーム遷移のコールバック
        self.canvas = tk.Canvas(self, width = self.width, height = self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)#canvasをmasterいっぱいに配置
        self.buttons = []
        self.last_active_obj = None

    def _calc_area(self, button_size_ratio, center_x_ratio, center_y_ratio):
        button_size_half = (button_size_ratio * self.width) / 2
        min_x = center_x_ratio * self.width - button_size_half
        max_x = center_x_ratio * self.width + button_size_half
        min_y = center_y_ratio * self.height - button_size_half
        max_y = center_y_ratio * self.height + button_size_half
        return (min_x, min_y, max_x, max_y)
    
    
class ControlFrame(BaseFrame):# 操作画面
    def __init__(self, master = None, app_instance = None):
        super().__init__(master,  app_instance)
        self.canvas.config(bg="#ADD8E6")
        button_list = [
            (FORWARD, FORWARD_ACTIVE, FORWARD_LOCK, FORWARD_ATTENTION, 2/4, 1/6, 'w'),
            (CCW, CCW_ACTIVE, CCW_LOCK, CCW_ATTENTION, 1/4, 3/6, 'a'),
            (CW, CW_ACTIVE, CW_LOCK, CW_ATTENTION, 3/4, 3/6, 'd'),
            (STOP, STOP_ACTIVE, STOP_LOCK, STOP_ATTENTION, 2/4, 3/6, 's'),
            (BACK, BACK_ACTIVE, BACK_LOCK, BACK_ATTENTION, 2/4, 5/6, 'z'),
        ]
        
        for img, active, lock, attention, center_x_ratio, center_y_ratio, cmd in button_list:
            area = self._calc_area(BUTTON_SIZE_RATIO, center_x_ratio,center_y_ratio)
            self.buttons.append(ControlButton(self.canvas, img, active, lock, attention, area, cmd))
        #設定ボタンについて
        area = self._calc_area(SETTING_SIZE_RATIO, 9/10, 8/10)
        self.buttons.append(ControlButton(self.canvas, SETTING, SETTING_ACTIVE, '_', SETTING_ATTENTION, area, 'g'))
        self.check_cursor()
    def check_cursor(self):
        x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        y = self.master.winfo_pointery() - self.master.winfo_rooty()

        #各ボタンにマウス位置を通知
        active_obj = None#新たにアクティブになったボタンのオブジェクト
        for button in self.buttons:
            active_cmd = button.update(x,y)
            if active_cmd == 'g':
                self.app.show_frame(FrameName.SETTINGS)
            if active_cmd is not None:#新たにアクティブになったボタンがあるなら
                active_obj = button#アクティブなボタンのオブジェクトを保存
        #全体のボタン状態の管理
        if active_obj:
            if self.last_active_obj and self.last_active_obj != active_obj:
                self.last_active_obj.set_nomal()
            self.last_active_obj = active_obj
        else:
            pass
        self.master.after(20, self.check_cursor)
class SettingFrame(BaseFrame):
    def __init__(self, master = None, app_instance = None):
        super().__init__(master, app_instance)
        self.canvas.config(bg="#98FB98")
        
        # === 速度表示テキスト ===
        cx = self.width * 2/4
        cy = self.height * 3/6
        self.canvas.create_text(cx, cy - 100, text="Speed", font=("Arial", 30))
        # テキストIDを保存して後で書き換えられるようにする
        self.speed_text_id = self.canvas.create_text(cx, cy, text=str(self.app.speed), font=("Arial", 80, "bold"))

        button_list = [
            (PLUS, PLUS_ACTIVE, '_', PLUS_ATTENTION, 1/4, 3/6, '+'),
            (MINUS, MINUS_ACTIVE, '_', MINUS_ATTENTION, 3/4, 3/6, '-'),
        ]
        for img, active, lock, attention, center_x_ratio, center_y_ratio, cmd in button_list:
            area = self._calc_area(BUTTON_SIZE_RATIO, center_x_ratio,center_y_ratio)
            self.buttons.append(SpeedButton(self.canvas, img, active, lock, attention, area, cmd))
        
        #設定ボタンについて
        area = self._calc_area(SETTING_SIZE_RATIO, 9/10, 2/10)
        self.buttons.append(ControlButton(self.canvas, SETTING, SETTING_ACTIVE,'_', SETTING_ATTENTION, area, 'g'))
        self.check_cursor()

    def update_speed_display(self):
        self.canvas.itemconfig(self.speed_text_id, text=str(self.app.speed))

    def check_cursor(self):
        x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        y = self.master.winfo_pointery() - self.master.winfo_rooty()

        #各ボタンにマウス位置を通知
        active_obj = None#新たにアクティブになったボタンのオブジェクト
        for button in self.buttons:
            active_cmd = button.update(x,y)#今フレームでアクティブになったボタン
            if active_cmd == 'g':
                self.app.show_frame(FrameName.CONTROL)#controlに遷移
                return
            elif active_cmd == '+':
                if self.app.speed < MAX_SPEED:
                    self.app.speed += 1
                    self.update_speed_display()
            elif active_cmd == '-':
                if self.app.speed > 0:
                    self.app.speed -= 1
                    self.update_speed_display()

            if active_cmd is not None:#新たにアクティブになったボタンがあるなら
                active_obj = button#アクティブなボタンのオブジェクトを保存
        #全体のボタン状態の管理
        if active_obj:#新たにアクティブになったボタンがあるなら
            if self.last_active_obj and self.last_active_obj != active_obj:
                self.last_active_obj.set_nomal()
            self.last_active_obj = active_obj
        else:
            pass
        self.master.after(20, self.check_cursor)

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
        if self.arc_id:
            self.canvas.delete(self.arc_id)
        angle = percent * 3.6
        self.arc_id = self.canvas.create_arc(
            x - self.arc_radius, y - self.arc_radius,
            x + self.arc_radius, y + self.arc_radius,
            start = 90, extent=-angle, style = 'pieslice',
            outline = 'white', fill = 'black'
        )

    def set_attention(self):
        #ボタンをattentionにする
        self.canvas.itemconfig(self.image_id, image=self.img_attention)

    def set_nomal(self):
        #ボタンをnomalにする
        #各変数を初期化する
        self.enter_time=None
        self.active = False
        if self.arc_id:
            self.canvas.delete(self.arc_id)
            self.arc_id = None
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
        if self.active:#アクティブなら、何もしない
            return None
        x1, y1, x2, y2 = self.area
        if x1 <= cursor_x <= x2 and y1 <= cursor_y <= y2:#カーソルが領域内部なら
            if self.enter_time is None:
                self.enter_time = time.time()
            elapsed = time.time() - self.enter_time
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

class SpeedButton(ControlButton):
    def __init__(self, canvas, img_path, active_path, lock_path, attention_path, area, cmd):
        super().__init__(canvas, img_path, active_path, lock_path, attention_path, area, cmd)
    def update(self, cursor_x, cursor_y):#カーソルのxy座標を受け取る
        x1, y1, x2, y2 = self.area
        if self.active:#アクティブなら
            if x1 <= cursor_x <= x2 and y1 <= cursor_y <= y2:
                return None
            else:
                self.set_nomal()
                return None
        if x1 <= cursor_x <= x2 and y1 <= cursor_y <= y2:#カーソルが領域内部なら
            if self.enter_time is None:
                self.enter_time = time.time()
            elapsed = time.time() - self.enter_time
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
class mainApp:
    def __init__(self):
        #全体で共有するデータを定義
        self.root = tk.Tk()
        self.root.title('eye controll')
        self.root.state("zoomed")
        self.current_frame = None#現在表示中のフレーム
        self.speed = DEFAULT_SPEED
        self.show_frame(FrameName.CONTROL)

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
        if frame_name == FrameName.CONTROL:
            self.current_frame = ControlFrame(self.root, self)
        elif frame_name == FrameName.SETTINGS:
            self.current_frame = SettingFrame(self.root, self)
    def run(self):
        self.root.mainloop()

def main():
    app = mainApp()
    app.run()

if __name__ == '__main__':
    main()