'''
Ez Scanner (Ez Sniffer + send_udp_message)
'''
import ipaddress
import os
import socket
import struct 
import sys
import threading
import config

message = config.MESSAGE
subnet = config.SUBNET

class ICMP(object):
    '''ICMP Header'''
    def __init__(self,buff=None) -> None:
        header = struct.unpack('<BBHHH',buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

class IP(object):
    '''struct of IP header'''
    def __init__(self,buff=None) -> None:
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        #! B (Byte)     : unsigned char (1 Byte)
        #! H (Half-Word): unsigned short (2 Byte)
        #! 4s(String)   : 4-Byte-long string
        self.ver = header[0] >> 4
        #! 获取高4位
        self.ihl = header[0] & 0xF
        #! 0xF 是 00001111 , 按位与获取低4位
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {
            1 : "ICMP" ,
            6 : "TCP" ,
            17: "UDP"
        }
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception:
            print(f"{Exception} ")
            print(f"Unsupported protocol number {self.protocol_num}")

def udp_sender():
    '''send udp messgaes to local network'''
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(subnet).hosts():
            sender.sendto( bytes(message,"utf-8") , (str(ip),65212) )

class Scanner(object):
    '''scan subnet info'''
    def __init__(self,host:str) -> None:
        self.host = host
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
        self.socket.bind((host,0))
        self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
        if os.name == "nt":
            self.socket.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    def sniff(self):
        '''do sniffing to recv echo messages'''
        hosts_up = set([f"{str(self.host)}*"])
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset+8]
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(subnet):
                            if raw_buffer[len(raw_buffer) - len(message)] == bytes(message,"utf-8"):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f"Host Up : {tgt}")
        except KeyboardInterrupt:
            if os.name == "nt":
                self.socket.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
            print("\nUser Interrupted")
            if hosts_up:
                print(f"\n\nSummary: Hosts up on {subnet}")
            for host in sorted(hosts_up):
                print(f"{host}")
            print('')
            sys.exit()

def main():
    '''entrance of scanner'''
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = config.HOST
    scanner = Scanner(host)
    threading.Thread(target = udp_sender).start()
    scanner.sniff()
if __name__ == "__main__":
    main()
