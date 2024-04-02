'''
Date: 2024-04-02 20:18:39
LastEditTime: 2024-04-02 20:18:41
Description: 业务逻辑的视图函数，封装成views.py
'''
from time import ctime
from typing import Optional
def index(env) -> Optional[str]:
    '''
    response /index request
    '''
    print(ctime())
    print(env)
    return "HelloWorld!"

def error(env) -> Optional[str]:
    '''
    response error request
    '''
    print(ctime())
    print(env)
    return "404 Not Found!"
