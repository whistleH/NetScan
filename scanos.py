from utils import *
import re
from scapy.all import *


# 使用TTL值判断OS类型
def ttl_scan(ip):
    ttlstrmatch = re.compile(r'ttl=\d+')
    ttlnummatch = re.compile(r'\d+')

    icmp_packet = IP(dst=ip)/ICMP()/b'whistleH'

    resp = sr1(icmp_packet, timeout=2, verbose=False)

    if resp:
        if int(resp.ttl) <= 64:
            print("Linux/Unix")
        else:
            print("Windows")
    else:
        print("No ping!")

ttl_scan("192.168.80.140")
