'''
TCP Agent Demo
'''
import sys
import socket
import threading

#可打印的字符字符表示长度为3个字符，利用生成器生成一个不可打印字符表示为.的ASCII码表
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)

def hexdump(src,length=16,show=True):
    '''
    接收bytes或string输入，转化为16进制格式返回或输出
    '''
    if isinstance(src,bytes):
        src = src.decode()

    results = list()
    for i in range(0,len(src),length):
        word = src[i:i+length]
        printtable = word.translate(HEX_FILTER)
        hexa = ' '.join([f"{ord(c):02X}" for c in word])
        hexwidth = length*3
        results.append(f"{i:04x} {hexa:<{hexwidth}} {printtable}")
    if show:
        for line in results:
            print(line)
    else:
        return results

def receive_from(connection:socket.socket) -> bytes:
    '''
    传入socket对象，返回该socket接收的数据
    '''
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception:
        pass
    return buffer

def request_handler(buffer):
    '''
    对接受的数据包进行某种处理
    '''
    return buffer

def response_handler(buffer):
    '''
    对响应的数据包进行某种处理
    '''
    return buffer

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
    '''
    连接远程主机，如果有打招呼环节(ftp)，就先接收数据。然后转发数据包直到读不到数据为止
    '''
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print(f"[<==] Sending {len(remote_buffer)} bytes to localhost.")
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line =  f"[==>] Received {len(remote_buffer)} bytes from localhost."
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer) :
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing Connection")
            break

def server_loop(local_host,local_port,
                remote_host,remote_port,receive_first):
    '''
    接收代理双方地址信息，进行代理转发
    '''
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.bind((local_host,local_port))
    except Exception :
        print(f"problem on bind:{Exception}")
        print(f"[!!] Failed to listen on {local_host}:{local_port}.")
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print(f"[*] Listening on {local_host}:{local_port}.")
    server.listen(5)

    while True:
        client_socket , addr = server.accept()
        print(f"> Received incoming connection from {addr[0]}:{addr[1]}")
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket,remote_host,remote_port,receive_first)
        )
        proxy_thread.start()

def main():
    '''程序入口'''
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]",end='')
        print("[remotehost] [remoteport] [receive_first](True or False)")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    if receive_first == "True":
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host,local_port,
                remote_host,remote_port,receive_first)

if __name__ == "__main__":
    main()
