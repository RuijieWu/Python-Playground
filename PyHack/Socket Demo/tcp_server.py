'''
TCP Socket Program Demo
'''
import socket
import threading

def handle_client(client_socket):
    '''show info'''
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        sock.send(b"ACK")

def main():
    '''entrance'''
    IP = ''
    PORT = 9998

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")

    while True:
        client,address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
