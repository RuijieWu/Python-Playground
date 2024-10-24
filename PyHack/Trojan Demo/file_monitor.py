'''
http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
'''
import os
import tempfile
import threading
import win32con
import win32file
import time

FILE_CREATED        = 1
FILE_DELETED        = 2
FILE_MODIFIED       = 3
FILE_RENAMED_FROM   = 4
FILE_RENAMED_TO     = 5
FILE_LIST_DIRECTORY = 0x0001
LOG_PATH = "./loginfo.csv "
#! 监控的文件夹路径列表
PATHS = ["c:\\WINDOWS\\TEMP",tempfile.gettempdir()]

def log_to_file(message:str) -> None:
    '''save log info'''
    with open(LOG_PATH,"w") as f:
        f.write(f"{time.ctime()}\r\n{message}\r\n")

def monitor(path_to_watch:str) -> None:
    '''Monitor'''
    #! 获取句柄
    h_directory = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    while True:
        try:
            #! 监控目录中出现的改动
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | 
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME | 
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY |
                win32con.FILE_NOTIFY_CHANGE_SIZE,
                None,
                None
            )
            #! 根据改动的类型进行输出
            for action , file_name in results:
                full_filename = os.path.join(path_to_watch,file_name)
                if action == FILE_CREATED :
                    print(f"[+] Created {full_filename}")
                elif action == FILE_DELETED :
                    print(f"[+] Deleted {full_filename}")
                elif action == FILE_MODIFIED :
                    print(f"[+] Modified {full_filename}")
                    try:
                        print("Dumping contents")
                        with open(full_filename) as f:
                            contents = f.read()
                        print(contents)
                        print("Dump completed")
                    except Exception:
                        print(f"[!] Dump failed {Exception}")
                elif action == FILE_RENAMED_FROM :
                    print(f"[+] Renamed from {full_filename}")
                elif action == FILE_RENAMED_TO :
                    print(f"[+] Renamed to {full_filename}")
                else:
                    print(f"[+] Unknown action on {full_filename}")
        except Exception:
            pass

if __name__ == "__main__":
    for path in PATHS :
        monitor_thread = threading.Thread(target=monitor,args=(path,))
        monitor_thread.start()