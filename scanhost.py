#coding:utf-8
from scapy.all import *
from random import randint
from optparse import OptionParser
from utils import *
import threading
import queue
import time
import concurrent.futures

class HostScanner():
    # 初始化参数
    def __init__(self, ips, scan_func, **kwargs):
        self._ips = ips
        self._scan_func =  scan_func
        self._scan_res = {}

        if 'iface' in kwargs.keys():
            self._iface = kwargs['iface']
        else:
            self._iface = ''
        if 'src_mac' in kwargs.keys():
            self._src_mac = kwargs['src_mac']
        else:
            self._src_mac = ''
        if 'thread_limit' in kwargs.keys():
            self._thread_limit = kwargs['thread_limit']
        else:
            self._thread_limit = 5
    
    def scanner(self,ip_index, ip, iface, src_mac):
        if self._scan_func == arp_scan:
            self._scan_res[ip_index] = (ip, self._scan_func(ip,iface,src_mac))
        else:
            self._scan_res[ip_index] = (ip, self._scan_func(ip))
    
    # 多线程运行
    def sacnner_helper(self):
        ip_index = 0
        while ip_index < len(self._ips):
            while threading.activeCount() <= self._thread_limit and ip_index < len(self._ips):
                thread = threading.Thread(target=self.scanner,
                                          args=(ip_index, self._ips[ip_index], self._iface, self._src_mac))
                thread.start()
                ip_index += 1

            time.sleep(0.5)

    # 多线程，线程池运行
    def start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._thread_limit) as executor:
            args_set = [[ip_index, self._ips[ip_index], self._iface, self._src_mac] for ip_index in range(len(self._ips))]
            scan_res = [executor.submit(lambda p: self.scanner(*p),args) for args in args_set]
            [f.result() for f in scan_res]
        return self._scan_res
        

# 构造ICMP包完成主机状态的检测
# 输入：待检测的IP
# TODO: up 返回True,down 返回false
def icmp_scan(ip):
    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)

    icmp_packet = IP(dst=ip,ttl=128,id=ip_id)/ICMP(id=icmp_id,seq=icmp_seq)/b'test_data'
    
    result = sr1(icmp_packet, timeout=2, verbose=False)
    if result:
        return True
    else:
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
    else:
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
        if resp[TCP].flags in ["RA", "SA"]:
            return True
            # print(ip + "--> Host is up")
    else:
        return False
        # print(ip + "--> Host is down")
    return False


# 构造UDP包完成主机的检测
def udp_scan(ip):
    # todo, 剔除常见端口
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


# demo
ips = ["127.0.0.1"]
hostscannner = HostScanner(ips,icmp_scan,thread_limit=5)
res = hostscannner.start()
print(res)

# 输出格式：{ip: T/F}
