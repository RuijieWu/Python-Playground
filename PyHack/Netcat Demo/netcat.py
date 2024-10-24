'''
NetCat Ez Demo
'''
import argparse
import config
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute_command(command) -> string :
    '''执行命令并返回命令执行结果'''
    cmd = command.strip()
    if not cmd :
        return
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    return output.decode()

class NetCat(object):
    '''NetCat 实现'''
    def __init__(self,args,buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)

    def run(self):
        '''执行入口'''
        if self.args.listen:
            slef.listen()
        else:
            self.send()

    def send(self):
        '''从标准输入读入数据发送至接收端并打印响应内容'''
        self.socket.connect((self.args.target,self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                rec_len = 1
                response =''
                while rec_len:
                    data = self.socket.recv(config.BUFFER_MAX_SIZE)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < config.BUFFER_MAX_SIZE:
                        break
                if response:
                    print(response)
                    buffer = input('>')
                    buffer += '\n'
                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            #'''捕获Ctrl + C关闭程序'''
            print('User terminated')
            self.socket.close()
            sys.exit()

    def listen(self):
        '''通过socket获取信息再并发进行处理'''
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)

        while True:
            client_socket , _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle , args = (client_socket,)
            )
            client_thread.start()

    def handle(self,client_socket):
        '''根据获取到的参数实现对应功能'''
        if self.args.execute:
            output = execute_command(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b""

            while True:
                data = client_socket.recv(config.BUFFER_MAX_SIZE)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload,'wb') as f:
                f.write(file_buffer)
            message = f"Saved file {self.args.upload}"
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b""

            while True:
                try:
                    client_socket.sned(b"BHP: #>")
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute_command(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b""
                except Exception:
                    print(f"server killed {Exception}")
                    self.socket.close()
                    sys.exit()

def main():
    '''作为命令解析的中间层向NetCat传递指令'''
    parser = argparse.ArgumentParser(
        description="BHP Net Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''  Example:
            netcat.py -t 192.168.1.108 -p 7777 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 7777 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 7777 -l -e=\"cat /etc/passwd\" # excute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 7777 # connect to server
            '''

        )
    )
    parser.add_argument('-c' , '--command' , action='store_true' , help='command shell')
    parser.add_argument('-e' , '--execute' , help='excute specified command')
    parser.add_argument('-l' , '--listen' , action='store_true' , help='listen')
    parser.add_argument('-p' , '--port' , type=int,default=7777 , help='specified port')
    parser.add_argument('-t' , '--target' , default='192.168.1.108' , help='specified IP')
    parser.add_argument('-u' , '--upload' , help = 'upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args,buffer.encode())

    nc.run()

if __name__ == "__main__":
    main()
