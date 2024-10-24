'''
TCP Socket Program Demo
'''
import socket

if __name__ =="__main__":
    TARGET_HOST = "www.baidu.com"
    TARGET_PORT = 80
    TARGET_PATH = "/"
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    client.connect((TARGET_HOST,TARGET_PORT))

    package = f"GET {TARGET_PATH} HTTP/1.1\r\nHost: {TARGET_HOST}\r\n\r\n"

    client.send(package.encode())

    response = client.recv(4096)

    print(response.decode())
    client.close()
