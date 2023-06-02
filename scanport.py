from utils import *

port_status = {
    0 : "Close",
    1 : "Open",
    2 : "filtered",
    3 : "unfiltered"
}

# ACK 扫描
def ack_scan(ip, ports):
    ports_s = {}
    for dport in ports:
        ack_packet = IP(dst=ip)/TCP(flags="A",dport = dport)
        resp = sr1(ack_packet, timeout=1, verbose=False)

        if resp is None:
            ports_s[dport] = port_status[2]
        elif resp:
            if resp.haslayer("ICMP") and resp["ICMP"].type==3:
                ports_s[dport] = port_status[2]
            if resp["TCP"].flags == 'R':
                ports_s[dport] = port_status[3]    
    return ports_s
    

# SYN 扫描
def syn_scan(ip, ports):
    ports_s = {}
    for dport in ports:
        syn_packet = IP(dst=ip)/TCP(flags="S",dport = dport)
        resp = sr1(syn_packet, timeout=1, verbose=False)

        if resp:
            if resp["TCP"].flags == "SA":
                ports_s[dport] = port_status[1]
            elif resp["TCP"].flags == "RA" : 
                ports_s[dport] = port_status[0]
    return ports_s

# NULL 扫描
# 测试对kali有效
def null_scan(ip ,ports):
    ports_s = {}
    for dport in ports:
        null_packet = IP(dst=ip)/TCP(flags='',dport = dport)
        resp = sr1(null_packet, timeout=2, verbose = False)
        # print(resp)
        if resp is None:
            ports_s[dport] = port_status[1] + "|" + port_status[2]
        else:
            if resp["TCP"].flags == "RA":
                ports_s[dport] = port_status[0]
    return ports_s

# FIN 扫描
def fin_scan(ip ,ports):
    ports_s = {}
    for dport in ports:
        null_packet = IP(dst=ip)/TCP(flags='F',dport = dport)
        resp = sr1(null_packet, timeout=2, verbose = False)
        # print(resp)
        if resp is None:
            ports_s[dport] = port_status[1] + "|" + port_status[2]
        else:
            if resp["TCP"].flags == "RA":
                ports_s[dport] = port_status[0]
    return ports_s


# Xmas 扫描
def xmas_scan(ip ,ports):
    ports_s = {}
    for dport in ports:
        null_packet = IP(dst=ip)/TCP(flags='PFU',dport = dport)
        resp = sr1(null_packet, timeout=2, verbose = False)
        # print(resp)
        if resp is None:
            ports_s[dport] = port_status[1] + "|" + port_status[2]
        else:
            if resp["TCP"].flags == "RA":
                ports_s[dport] = port_status[0]
    return ports_s

ip = "192.168.80.140"
ports = [22, 80, 443, 1234, 3389]
print(syn_scan(ip, ports))