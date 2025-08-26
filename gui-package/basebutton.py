import tkinter as tk
from config.filepath import CW, CW_ACTIVE, CW_ATTENTION, CW_LOCK
from config.filepath import CCW, CCW_ACTIVE, CCW_ATTENTION, CW_LOCK
from config.filepath import BUTTONS
from typing import TypedDict

class BaseButton:
    def __init__(self, name = None, area = None, cmd = None):
        self.name = name
        print(BUTTONS['forward']['normal'])

def main():
    print('test')
    a = BaseButton()


if __name__ == '__main__':
    main()
