'''
EZ Sniffer
'''
import ipaddress
import socket
import struct
import os
import sys
import config


#! Ipv4 Header
#! offset   |  0-3  |  4-7  |  8-15  |  16-18  |  19-31  |
#!   0      | 版本   | 头长度| 服务类型|     总长度        |
#!   32     |          标识          |   标志   | 段偏移  |
#!   64     |     TTL       | 协议    |     头校验和      |
#!   96     |                  源IP地址                  |
#!   128    |                  目的IP地址                 |
#!   160    |                   其它可选参数              |
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

#! ICMP
#! 0     4     8     12     16     20     24     28     32
#!|    类型    |    代码     |           校验和           |
#!|           标识          |            序列编号        |
#!|                       可选数据                       |
class ICMP(object):
    '''ICMP Header'''
    def __init__(self,buff=None) -> None:
        header = struct.unpack('<BBHHH',buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

def sniff(host:str):
    '''sniff from socket'''
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
    sniffer.bind((host,80))
    #! 抓包时包含IP头
    sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
    #! 如果是WIndows系统就发送IOCTL启用网卡混杂模式
    if os.name=="nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ip_header = IP(raw_buffer[0:20])
            if ip_header.protocol == "ICMP":
                print(f"Protocol: {ip_header.protocol}    {ip_header.src_address} -> {ip_header.dst_address}")
                print(f"Version: {ip_header.ver}")
                print(f"Header Length : {ip_header.len}")
                print(f"TTL : {ip_header.ttl}")
                
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]
                icmp_header = ICMP(buf)
                print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}")
            else:
                print(f"Protocol: {ip_header.protocol}    {ip_header.src_address} -> {ip_header.dst_address}")
    except KeyboardInterrupt:
        if os.name == "nt" :
            sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
        sys.exit()


def main():
    '''Entrance of Sniffer'''
    if len(sys.argv) == 2 :
        host = sys.argv[1]
    else :
        host = config.HOST

    sniff(host)

if __name__ == "__main__":
    main()
