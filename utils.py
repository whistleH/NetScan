#coding:utf-8
from scapy.all import *
import psutil
from config import OS_DB,OS_SIGNS


def get_iface_name():
    if_list = psutil.net_if_addrs()
    return [x for x in if_list.keys()]

def get_os_from_ttl(ttl):
    # 反向求取真实ttl
    os_ttl = 1 if ttl == 0 else 2**(ttl - 1).bit_length()
    os_set = set(OS_SIGNS["TTL"][os_ttl])
    return os_set


def get_os_from_df(df):
    os_set = set(OS_SIGNS["DF"][df])
    return os_set


def get_os_from_icmp(ttl,df):
    os_set = get_os_from_df(df) & get_os_from_ttl(ttl)
    return os_set


def get_os_from_winsize(win_size):
    if win_size in OS_SIGNS["Win_Size"].keys():
        return set(OS_SIGNS["Win_Size"][win_size])
    
    if 2920 <= win_size <= 5840:
        return set(["Linux"])
    
    return set(["Windows XP", "Windows 7", "Windows 10"])


def get_os_from_mss(mss):
    if mss in OS_SIGNS["MSS"].keys():
        os_set = set(OS_SIGNS["MSS"][mss])
    else:
        os_set = set(OS_DB)
    return os_set

def get_os_from_tcp(win_size,mss):
    os_set = get_os_from_winsize(win_size) & get_os_from_mss(mss)
    return os_set

def get_user_agent():
    options = []
    with open('db/user-agents.txt','r') as fin:
        lines = fin.readlines()
        for i in lines:
            options.append(i.strip())
    return options



