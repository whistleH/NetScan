#coding:utf-8
from scapy.all import *
import psutil

port_status = {
    0 : "Close",
    1 : "Open",
    2 : "filtered",
    3 : "unfiltered"
}

def get_iface_name():
    if_list = psutil.net_if_addrs()
    return [x for x in if_list.keys()]

