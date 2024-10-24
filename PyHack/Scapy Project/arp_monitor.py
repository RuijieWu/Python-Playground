'''
Date: 2024-02-11 02:10:56
LastEditTime: 2024-04-03 14:05:58
Description: 
'''
import sys
from signal import signal,SIGINT
from time import ctime
from scapy.all import sniff
from scapy.layers.l2 import ARP

ARP_MONITOR_DB_FILE = "./1.db"
ip_mac = {}

def sig_int_handler(signum,frame) -> None:
    '''recall handler'''
    print("[*] Get SIGINT.Saving ARP database...")
    print(ctime())
    try:
        f = open(ARP_MONITOR_DB_FILE,"w",encoding="utf-8")
        for ip,mac in ip_mac.items():
            f.write(f"{ip} {mac}\n")
        f.close()
        print("[*] Done")
        print(ctime())
    except IOError:
        print(f"[*] Cannot Open {ARP_MONITOR_DB_FILE}")
    sys.exit(1)

def watch_arp(pkt):
    '''monitor'''
    if pkt[ARP].op == 2:
        print(f"{pkt[ARP].hwsrc} {pkt[ARP].psrc}")
        if not ip_mac.get(pkt[ARP].psrc) :
            print(f"[*] Found new device {pkt[ARP].hwsrc} {pkt[ARP].psrc}")
            ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc
        elif ip_mac.get(pkt[ARP].psrc) and \
            ip_mac[pkt[ARP].psrc] != pkt[ARP].hwsrc:
            print(
                f"{pkt[ARP].hwsrc} has got new ip {pkt[ARP].psrc}" + \
                f"(old {ip_mac[pkt[ARP].psrc]})"
                )
            ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc

def main():
    '''entrance'''
    signal(SIGINT,sig_int_handler)
    if len(sys.argv) < 2:
        print("[*] Incorrect arguments number")
        sys.exit(0)
    try:
        fh = open(ARP_MONITOR_DB_FILE,"r",encoding="utf-8")
    except IOError:
        print(f"[*] Cannot read {ARP_MONITOR_DB_FILE}")
        sys.exit(1)
    for line in fh:
        line.chomp()
        ip , mac = line.split(' ')
        ip_mac[ip] = mac
    sniff(prn=watch_arp,filter="arp",iface=sys.argv[1],store=0)

if __name__ == "__main__":
    main()
