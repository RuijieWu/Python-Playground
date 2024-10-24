'''
Deal pcap file and save images
'''
import collections
import os
import re
import sys
import zlib
from scapy.all import (
    TCP,
    rdpcap
)
#! 文件保存路径和PCAP文件路径
OUTDIR = ""
PCAPS = ""
Response = collections.namedtuple("Response",["Header","Payload"])

def get_header(payload:bytes)->dict:
    '''提取头部'''
    try:
        hedaer_raw = payload[:payload.index(b'\r\n\r\n')+2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    header= dict(re.findall(r"(?P<name>.*?):(?P<value>.*?)\r\n",hedaer_raw.decode()))
    if "Content-Type" not in header:
        return None
    return header

def extract_content(Response,content_name)->tuple:
    '''提取内容'''
    content , content_type = None , None
    if content_name in Response.header["Content-Type"]:
        content_type = Response.header["Content-Type"].split('/')[1]
        content = Response.payload[Response.payload.index(b"\r\n\r\n")+4:]
        if "Content-Encoding" in Response.header:
            #!若响应数据被压缩过则解压
            if Response.header["Content-Encoding"] == "gzip":
                content = zlib.decompress(Response.payload,zlib.MAX_WBITS | 32)
            elif Response.header["Content-Encoding"] == "deflate":
                conteng = zlib.decompress(Response.payload)
    return content,content_type      

class Recapper(object):
    '''提取并保存数据包内的文件信息并保存到本地'''
    def __init__(self,filename) -> None:
        pcap = rdpcap(filename)
        self.sessions = pcap.sessions()
        self.responses = list()
    def get_responses(self):
        '''读取并处理响应数据'''
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    if packet["TCP"].dport == 80 or packet["TCP"].sport == 80:
                        payload += bytes(packet["TCP"].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()
            if payload:
                header = get_header(payload)
                if not header:
                    continue
                self.responses.append(Response(header,payload))
    def write(self,content_name):
        '''保存提取出的内容'''
        for i,response in enumerate(self.responses):
            content , content_type = extract_content(response,content_name)
            if content and content_type:
                filename = os.path.join(OUTDIR + f"ex_{i}.{content_type}")
                with open(filename,"wb") as f:
                    f.write(content)

def main():
    '''entrance of the program'''
    pfile = os.path.join(PCAPS,'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write("image")

if __name__ == "__main__":
    main()
