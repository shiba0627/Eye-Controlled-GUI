import base
import tkinter as tk
DEFAULT_SPEED = 4


class App:
    def __init__(self):
        #全体で共有するデータを定義
        self.root = tk.Tk()
        self.root.title('eye controll')
        self.root.state("zoomed")
        self.current_frame = None#現在表示中のフレーム
        self.speed = DEFAULT_SPEED
        self.show_frame(base.FrameName.CONTROL)

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
        if frame_name == base.FrameName.CONTROL:
            self.current_frame = base.ControlFrame(self.root, self)
        elif frame_name == base.FrameName.SETTINGS:
            self.current_frame = base.SettingFrame(self.root, self)
    def run(self):
        self.root.mainloop()
def main():
    app = App()
    app.run()

if __name__ == '__main__':
    main()