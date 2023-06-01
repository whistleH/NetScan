#coding:utf-8
from scapy.all import *
import psutil


def get_iface_name():
    if_list = psutil.net_if_addrs()
    return [x for x in if_list.keys()]

# print(get_iface_name())
# print(get_if_hwaddr('WLAN'))
