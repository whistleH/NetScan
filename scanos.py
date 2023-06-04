#coding:utf-8
from utils import *
import re
from scapy.all import *
import random


# 使用TTL值 和 DF值 判断OS类型
def icmp_para_scan(ip):
    icmp_packet = IP(dst=ip)/ICMP(type="echo-request")/b'test_data'

    resp = sr1(icmp_packet, timeout=2, verbose=False)

    if resp:
        ttl = resp[IP].ttl
        df = int(format(resp[IP].flags.value, "03b")[1])
        os_set = get_os_from_icmp(ttl, df)
        return {"ICMP":', '.join(os_set)}
    else:
        return {"ICMP":"主机无法PING通，请确认主机存活"}
    
# 这个方法需要输入有效端口号
def tcp_para_scan(ip, dport):
    syn_packet = IP(dst=ip)/TCP(flags="S", dport=dport)
    resp = sr1(syn_packet, timeout=2, verbose=False)
    if resp:
        ttl = resp[IP].ttl
        df = int(format(resp[IP].flags.value, "03b")[1])
        os_set = get_os_from_icmp(ttl, df)

        win_size = resp[TCP].window
        mss = dict(resp[TCP].options)["MSS"]
        os_set = os_set & get_os_from_tcp(win_size,mss)
        return {"TCP":', '.join(os_set)}
    else:
        return {"TCP":"主机端口无法进行TCP探测"}
    
# print(tcp_para_scan("192.168.80.140",80))


