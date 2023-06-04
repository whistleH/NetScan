#coding:utf-8
from utils import *
import time
import concurrent.futures
from scanservice import get_banner
from config import PORT_STATUS

class PortScanner():
    def __init__(self, ip, ports, scan_func, **kwargs):
        self._ip = ip
        self._ports = ports
        self._scan_func = scan_func
        self._scan_res = {}

        if 'thread_limit' in kwargs.keys():
            self._thread_limit = kwargs['thread_limit']
        else:
            self._thread_limit = 5
        
  
    def scanner(self, port_index, port, ip):
        status = self._scan_func(ip, port) 
        if status in [PORT_STATUS[1],PORT_STATUS[2],PORT_STATUS[3]]: 
            self._scan_res[port_index] = (port, status, get_banner(ip, port))
        else:
            self._scan_res[port_index] = (port, status, "")

    def start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._thread_limit) as executor:
            args_set = [[port_index, self._ports[port_index], self._ip] for port_index in range(len(self._ports))]
            scan_res = [executor.submit(lambda p: self.scanner(*p),args) for args in args_set]
            [f.result() for f in scan_res] 
        return self._scan_res

# ACK 扫描
def ack_scan(ip, dport):
    ack_packet = IP(dst=ip)/TCP(flags="A",dport = dport)
    resp = sr1(ack_packet, timeout=1, verbose=False)

    if resp is None:
        port_s = PORT_STATUS[2]
    elif resp:
        if resp.haslayer("ICMP") and resp["ICMP"].type==3:
            port_s = PORT_STATUS[2]
        if resp["TCP"].flags == 'R':
            port_s= PORT_STATUS[3]    
    return port_s  

# SYN 扫描
def syn_scan(ip, dport):
    syn_packet = IP(dst=ip)/TCP(flags="S",dport = dport)
    resp = sr1(syn_packet, timeout=1, verbose=False)
    if resp:
        if resp["TCP"].flags == "SA":
            port_s = PORT_STATUS[1]
        elif resp["TCP"].flags == "RA" or resp["TCP"].flags == "R": 
            port_s = PORT_STATUS[0]
    else:
        port_s = PORT_STATUS[0]
    return port_s

# FIN 扫描
def fin_scan(ip, dport):
    fin_packet = IP(dst=ip)/TCP(flags='F',dport = dport)
    resp = sr1(fin_packet, timeout=2, verbose = False)
    print(dport, resp)
    if resp is None:
        port_s = PORT_STATUS[1] + "|" + PORT_STATUS[2]
    else:
        if resp["TCP"].flags == "RA":
            port_s = PORT_STATUS[0]
    return port_s

# Xmas 扫描
def xmas_scan(ip ,dport):
    xmas_packet = IP(dst=ip)/TCP(flags='PFU',dport = dport)
    resp = sr1(xmas_packet, timeout=2, verbose = False)
    # print(resp)
    if resp is None:
        port_s = PORT_STATUS[1] + "|" + PORT_STATUS[2]
    else:
        if resp["TCP"].flags == "RA":
            port_s = PORT_STATUS[0]
    return port_s

# NULL 扫描
# 只对少数系统有效
def null_scan(ip ,dport):
    null_packet = IP(dst=ip)/TCP(flags='',dport = dport)
    resp = sr1(null_packet, timeout=2, verbose = False)
    # print(resp)
    if resp is None:
        port_s= PORT_STATUS[1] + "|" + PORT_STATUS[2]
    else:
        if resp["TCP"].flags == "RA":
            port_s = PORT_STATUS[0]
    return port_s


def get_scan_func(func_name):
    if func_name == "ACK":
        return ack_scan
    elif func_name == "SYN":
        return syn_scan
    elif func_name == "FIN":
        return fin_scan
    elif func_name == "XMAS":
        return xmas_scan
    else:
        return null_scan

# ip = "192.168.80.1"
# ports = [80,22,3389,443,3306]
# portscanner = PortScanner(ip, ports, syn_scan, thread_limit=1)
# res = portscanner.start()
# print(res)

# 输出格式：index:(port, status, service)
# {0: (22, 'Open', 'SSH'), 1: (80, 'Open', 'HTTP'), 2: (443, 'Close', ''), 3: (1234, 'Close', ''), 4: (3389, 'Close', '')}
