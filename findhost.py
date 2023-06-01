from scapy.all import *
from random import randint
from optparse import OptionParser


# 构造ICMP包完成主机状态的检测
# 输入：待检测的IP
# TODO: 输出格式的完善以及报错的完善
def icmp_scan(ip):
    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)

    icmp_packet = IP(dst=ip,ttl=128,id=ip_id)/ICMP(id=icmp_id,seq=icmp_seq)/b'whistleH'

    result = sr1(icmp_packet, timeout=2, verbose=False)
    if result:
        for rcv in result:
            scan_ip = rcv[IP].src
            print(scan_ip + "--> Host is up")
    else:
        print(ip + "--> Host is down")


def ack_scan(ip):
    # 随机端口，可能需要完善
    dport = random.randint(1, 65535)
    ack_packet = IP(dst=ip)/TCP(flags="A",dport = dport)
    resp = sr1(ack_packet, timeout=1, verbose=False)

    if resp:
        if resp[TCP].flags == "R":
            print(ip + "--> Host is up")
        else:
            print(ip + "--> Host is down")

# icmp_scan("192.168.80.140")
ack_scan("192.168.80.140")

