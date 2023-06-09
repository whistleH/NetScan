#coding:utf-8
from scapy.all import *
from utils import *
import json
import socket
import re
from config import SER_SIGNS

def banner_match(resp):
    if re.search(b'<title>502 Bad Gateway', resp):
        proto = "service uncessed!"
    for pattern in SER_SIGNS:
        pattern = pattern.split(b'|')
        if re.search(pattern[-1], resp, re.IGNORECASE):
            proto = pattern[1].decode()
            break
        else:
            proto = "Unrecognized"
    return proto


def get_banner(ip, port):
    reset_time = 0
    while True:
        resp = ''
        PROBE = 'GET / HTTP/1.0\r\n\r\n'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, int(port)))
        if result == 0:
            try:
                sock.sendall(PROBE.encode())
                resp = sock.recv(256)
                if resp:
                    sock.close()
                    return banner_match(resp)
                else:
                    reset_time += 1
                    if reset_time > 5:
                        sock.close()
                        return "Unrecognized/Reset" 
            except(ConnectionResetError, socket.timeout):
                print("reset")
                reset_time += 1
                if reset_time > 5:
                    sock.close()
                    return "Net fail/Reset"
                pass
        else:
            # 当端口无法关闭/禁止连接会触发这个分支
            # 服务判断前先应该先调用端口存活验证
            break
        sock.close()
        
# if __name__ == "__main__":
#     print(get_banner("127.0.0.1","3306"))

