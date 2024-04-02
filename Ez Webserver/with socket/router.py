'''
Date: 2024-04-02 15:48:37
LastEditTime: 2024-04-02 20:10:02
Description: 
'''
'''
Web server routeer and response to client
'''
from time import ctime
from http import HTTPStatus
import socket
import config
import parser

def index(conn:socket.socket,request: parser.Request) -> None:
    '''
    corresponding function
    '''
    response(conn,HTTPStatus.OK if request.path == "/" or "/index" else HTTPStatus.NOT_FOUND)

def response(conn: socket.socket,status_code: int) -> None:
    '''
    response message
    '''
    if status_code == HTTPStatus.NOT_FOUND:
        pass
    elif status_code == HTTPStatus.OK:
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
        conn.send(b'HelloWorld')


def route() -> None:
    '''
    the entrance of the server
    '''
    server = socket.socket()
    server.bind((config.SERVER_IP_ADDRESS,config.SERVER_PORT_NUMBER))
    server.listen(config.SERVER_BACKLOG)

    while True:
        conn , addr = server.accept()
        try:
            data = conn.recv(config.BUF_SIZE)
            data = data.decode('utf-8')
            request = parser.parse(data)
            request.addr = addr
            print(f"[*] {ctime()}\n{addr[0]}:{addr[1]} {request.method} {request.path}")
            if request.path == '/index' or "/":
                index(request=request,conn=conn)
        except socket.error:
            conn.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        except KeyboardInterrupt:
            print("Webserver terminated")
            break
        finally:
            conn.close()
