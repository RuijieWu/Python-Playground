'''
Sniff various protocols like HTTP by scapy frame
'''
from scapy.all import sniff
#! BPF Grammar
#!   descriptor       direction       protocol
#! host/net/port       src/dst     ip/ip6/tcp/udp
#! learn more PROTOCOL Ports on http://7erry.com/2020/03/30/%E5%B8%B8%E7%94%A8%E7%AB%AF%E5%8F%A3%E5%A4%87%E5%BF%98%E5%BD%95/
PROTOCOL_FILTERS = {
    "HTTP"  :   "tcp port 80 or tcp port 443 or udp port 80 or udp port 443",
    "SSH"   :   "tcp port 22",
    "TELNET":   "tcp port 23",
    "DHCP"  :   "tcp port 67 or tcp port 68",
    "SMTP"  :   "tcp port 25",
    "FTP"   :   "tcp port 21",
    "DNS"   :   "tcp port 53",
    "POP"   :   "tcp port 109 or tcp port 110"
}
def packet_callback(packet) -> None:
    '''show packet info'''
    try:
        if packet["TCP"].payload or packet["UDP"].payload:
            #!if "user" in str(packet['TCP'].payload).lower() or "pass" in str(packet["TCP"].payload).lower():
            print(f"[*] Destination: {packet['IP'].dst}")
            print(f"[*] {str(packet['IP'].payload)}")
    except IndexError:
        pass

def main():
    '''entrance'''
    #! HTTP as an example
    sniff(filter=PROTOCOL_FILTERS["HTTP"],prn=packet_callback,store = 0)

if __name__ == "__main__":
    main()
