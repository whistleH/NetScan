from scapy.all import *
from random import randint
from optparse import OptionParser

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



icmp_scan("192.168.80.123")

