'''
为了写脚本速通性质地学了学GDI编程
GDI是微软提供的图形界面的接口，屏幕上显示的内容本质上还是内存里的一块数据，截图就是把这些数据从内存中进行拷贝
为了拷贝屏幕内容，我们需要获取屏幕的句柄，一种特殊的指向特定内存区域的指针，然后通过提供句柄和屏幕参数调用GDI
Bitmap对象是屏幕内容的抽象与封装，设备/内存上下文是包含了其环境信息的特殊数据结构
'''
import win32api
import win32con
import win32gui
import win32ui

def get_demensions() -> tuple:
    '''获取屏幕尺寸'''
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width , height , left , top)

def screenshot(name="screenshot"):
    '''截图'''
    #! 获取桌面句柄
    hdesktop = win32gui.GetDesktopWindow()
    width , height , left , top = get_demensions()
    #! 创建设备上下文
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    #! 创建内存上下文
    mem_dc = img_dc.CreateCompatibleDC()
    #! 创建位图对象并初始化
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc,width,height)
    mem_dc.SelectObject(screenshot)
    #! 复制桌面图片到内存上下文中
    mem_dc.BitBlt(
        (0,0),
        (width,height),
        img_dc,
        (left,top),
        win32con.SRCCOPY
    )
    #! 内存 -> 磁盘
    screenshot.SaveBitmapFile(mem_dc,f"{name}.bmp")
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def main()->str:
    '''入口并提供截图读取功能'''
    screenshot()
    with open("screenshot.nmp") as f:
        img = f.read()
    return img

if __name__ == "__main__":
    main()
