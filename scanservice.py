from scapy.all import *
from utils import *
import json

signs = {
    "origin" : [b'FTP|FTP|^220.*FTP',
                b'MySQL|MySQL|mysql_native_password',
                b'oracle-https|^220 -ora',
                b'Telnet|Telnet|Telnet',
                b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
                b'VNC|VNC|^RFB',
                b'IMAP|IMAP|^\* OK.*?MAP',
                b'POP|POP|^\+OK.*?',
                b'SMTP|SMTP|^220.*?SMTP',
                
                ]
}