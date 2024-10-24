'''

'''
from ctypes import (
    byref,
    c_uint,
    c_ulong,
    sizeof,
    Structure,
    windll
)
import random
import sys
import time
import time
import win32api

class LASTINPUTINFO(Structure):
    fields_ = [
        ("cbSize",c_uint),
        ("dwTime",c_ulong)
    ]

def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
    run_time = windll.kernel32.GetTickCount()
    elapsed = run_time - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last event.")
    return elapsed

class Detector(object):
    def __init__(self) -> None:
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0
        
    def get_key_press(self):
        pass
    def detect(self):
        pass
    
if __name__ == "__main__":
    detector = Detector()
    detector.detect()
