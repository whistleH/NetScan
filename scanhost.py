#coding:utf-8
from scapy.all import *
from random import randint
from optparse import OptionParser
from utils import *


# 构造ICMP包完成主机状态的检测
# 输入：待检测的IP
# TODO: up 返回True,down 返回false
def icmp_scan(ip):
    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)

    icmp_packet = IP(dst=ip,ttl=128,id=ip_id)/ICMP(id=icmp_id,seq=icmp_seq)/b'whistleH'

    result = sr1(icmp_packet, timeout=2, verbose=False)
    if result:
        for rcv in result:
            scan_ip = rcv[IP].src
            return True
            #print(scan_ip + "--> Host is up")
    else:
        return False
        # print(ip + "--> Host is down")
    return False


# 构造ARP包完成主机的检测
def arp_scan(ip, iface, src_mac=''):
    if src_mac == '':
        src_mac = get_if_hwaddr(iface)

    arp_packet = Ether(src=src_mac, dst='FF:FF:FF:FF:FF:FF')/ARP(op=1,hwsrc=src_mac, hwdst='00:00:00:00:00:00',pdst=ip)
    # print(arp_packet)

    resp = srp(arp_packet, timeout = 1, iface=iface, verbose=False)
    # resp[0].res[0][1].fields['dst']
    if resp:
        return True
        # print(ip + "--> Host is up")
    else:
        return False
        # print(ip + "--> Host is down")
    return False


# 构造ACK包完成主机的检测
def ack_scan(ip):
    # 随机端口，可能需要完善，后续端口扫描完善
    dport = random.randint(1, 65535)
    ack_packet = IP(dst=ip)/TCP(flags="A",dport = dport)
    resp = sr1(ack_packet, timeout=1, verbose=False)

    if resp:
        if resp[TCP].flags == "R":
            return True
            # print(ip + "--> Host is up")
    else:
        return False
        # print(ip + "--> Host is down")
    return False


# 构造SYN包完成主机的检测
def syn_scan(ip):
    dport = random.randint(1, 65535)
    syn_packet = IP(dst=ip)/TCP(flags="S",dport = dport)
    resp = sr1(syn_packet, timeout=1, verbose=False)

    if resp:
        print(resp[TCP].flags)
        if resp[TCP].flags in ["RA", "R", "SA"]:
            return True
            # print(ip + "--> Host is up")
    else:
        return False
        # print(ip + "--> Host is down")
    return False


# 构造UDP包完成主机的检测
def udp_scan(ip):
    dport = random.randint(1, 65535)
    udp_packet = IP(dst=ip)/UDP(dport = dport)
    resp = sr1(udp_packet, timeout=1, verbose=False)

    if resp:
        if int(resp[IP].proto) == 1:
            return True
            # print(ip + "--> Host is up")
    else:
       return False
       # print(ip + "--> Host is down") 
    return False

# icmp_scan("192.168.80.140")
# ack_scan("192.168.80.140")
# syn_scan("192.168.80.140")
# arp_scan("192.168.80.123",'VMware Network Adapter VMnet8')

# ip = '192.168.80.140'
# if udp_scan(ip):
#     print(ip + "--> Host is up")
# else:
#     print(ip + "--> Host is down") 


