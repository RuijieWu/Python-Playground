'''
http://timgolden.me.uk/python/wmi/tutorial.html
'''
#!import os
#!import sys
#!import win32api
#!import win32con
#!import win32security
import wmi
import time

def log_to_file(message:str/tuple(str,str)) -> None:
    '''save log info'''
    with open("process_monitor_log.csv","a") as f:
        f.write(f"{time.ctime()}\r\n{message}\r\n")

def monitor() -> None:
    '''Mon1tor!'''
    HEAD = "CommandLine , Time , Executable , Parent PID , PID , User , Privileges"
    log_to_file(HEAD)
    #! 创建WMI实例
    c = wmi.WMI()
    #! 监控进程创建事件
    process_watcher = c.Win32_Process.watch_for("creation")
    while True:
        try:
            #! 等待process_watcher返回进程时间，然后读取其信息
            new_process = process_watcher()
            cmdline = new_process.CommandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner()
            
            privileges = "N/A"
            process_log_message = (
                f"{cmdline} , {create_date} , {executable}",
                f"{parent_pid} , {pid} , {proc_owner} , {privileges}"
            )
            print(process_log_message)
            print()
            log_to_file(process_log_message)
        except Exception:
            pass

if __name__ == "__main__":
    monitor()