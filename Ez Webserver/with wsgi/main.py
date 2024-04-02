'''
Date: 2024-04-02 20:18:12
LastEditTime: 2024-04-02 20:19:41
Description: entrance
'''
from wsgiref.simple_server import make_server
from router import urls
import views

def run(env,response):
    '''
    :param env: 请求相关的所有数据
    :param response: 响应相关的所有数据
    :return: 返回给浏览器的所有数据
    '''
    print(env)
    response('200 OK',[])
    current_path = env.get('PATH_INFO')
    func = None
    for url in urls:
        if current_path == url[0]:
            func = url[1]
            print(url[0])
            break
    if func:
        res = func(env)
    else:
        res = views.error(env)
    return [res.encode('utf-8')]

if __name__ == '__main__':
    server = make_server('127.0.0.1',8080,run)
    server.serve_forever()
