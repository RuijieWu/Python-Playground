'''
Date: 2024-01-21 00:08:06
LastEditTime: 2024-04-02 19:19:56
Description: parse http requests
'''
from enum import Enum
from typing import Optional

class Method(Enum):
    '''HTTP Method'''
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class Request(object):
    '''
    describe http request
    '''
    def __init__(
        self,
        method: Optional[Method] = None,
        path: Optional[str] = None,
        http_version: Optional[str] = None,
        host: Optional[str] = None,
        user_agent: Optional[str] = None,
        connection: Optional[bool] = None,
        cookie: Optional[str] = None
        ) -> None:
        self.method = method
        self.path = path
        self.host = host
        self.http_version = http_version
        self.user_agent = user_agent
        self.connection = connection
        self.cookie = cookie
        self.addr = None

def parse(request:str) -> Request:
    '''
    parse http request into a Request
    '''
    method = None
    path = None
    host = None
    http_version = None
    user_agent = None
    connection = None
    cookie = None

    try:
        args = request.split('\n')
        first_line = args.pop(0)
        first_line = first_line.split(' ')
        match first_line[0]:
            case "GET":
                method = Method.GET
            case "POST":
                method = Method.POST
            case "PUT":
                method = Method.PUT
            case "DELETE":
                method = Method.DELETE
            case _:
                method = None
        path = first_line[1]
        http_version = first_line[2]
        for argument in args:
            key = argument.split(':')[0]
            match key.lower():
                case "host":
                    host = argument.split(':')[1][1:]
                case "user-agent":
                    user_agent = argument.split(':')[1][1:]
                case "connection":
                    connection = True if \
                        argument.split(':')[1][1:].lower() == "keep-alive" \
                        else  False
                case "cookie":
                    cookie = argument.split(':')[1][1:]

    except IndexError:
        return Request()
    else:
        return Request(
            method = method,
            path = path,
            host = host,
            http_version = http_version,
            user_agent = user_agent,
            connection = connection,
            cookie = cookie
            )
