#coding:utf-8


DIR_DB = 'db'
DIR_LOG = 'log'

PORT_STATUS = {
    0 : "Close",
    1 : "Open",
    2 : "filtered",
    3 : "unfiltered"
}


SER_SIGNS = [       
            b'FTP|FTP|^220.*FTP',
            b'MySQL|MySQL|mysql_native_password',
            b'oracle-https|^220 -ora',
            b'Telnet|Telnet|Telnet',
            b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
            b'VNC|VNC|^RFB',
            b'IMAP|IMAP|^\* OK.*?MAP',
            b'POP|POP|^\+OK.*?',
            b'SMTP|SMTP|^220.*?SMTP',
            b'Kangle|Kangle|HTTP .*kangle',
            b'SMTP|SMTP|^554 SMTP',
            b'SSH|SSH|^SSH-',
            b'HTTPS|HTTPS|Location: https',
            b'HTTP|HTTP|HTTP/1.1',
            b'HTTP|HTTP|HTTP/1.0',
        ]

OS_DB = {"Linux", "FreeBSD", "Windows XP", "Windows 7", "Windows 10", "Symbian", "Palm OS", "Centos", "Ubuntu", "Debain"}

OS_SIGNS = {
	"DF": {
		1: {"FreeBSD", "Linux", "Windows XP", "Windows 7", "Windows 10", "Centos", "Ubuntu", "Debain"},
		0: {"FreeBSD", "Symbian", "Palm OS", "Linux", "Windows XP", "Windows 7", "Windows 10", "Centos", "Ubuntu"}
	},
	"TTL": {
		64:	{"Linux", "FreeBSD", "Centos", "Ubuntu"},
		128: {"Windows XP", "Windows 7", "Windows 10"},
		256: {"Symbian", "Palm OS", "Cisco IOS", "Debain"}
	},
	"Win_Size": {
		8192: {"Symbian", "Windows 7"},
		14600: {"Linux"},
		16348: {"Palm OS"},
		64240: {"Linux", "Ubuntu", "Centos"},
		65392: {"Windows 10"},
		65535: {"FreeBSD", "Windows XP", "Windows 10"},
		65550: {"FreeBSD"},
		29200: {"Centos"},
		26883: {"Debain"},
		None: {"Linux", "FreeBSD", "Windows XP", "Windows 7", "Windows 10", "Symbian", "Palm OS", "Centos", "Ubuntu", "Debain"}
	},
	"MSS": {
		1350: {"Palm OS"},
		1440: {"Windows XP", "Windows 7", "Windows 10"},
		1460: {"Linux", "FreeBSD", "Windows XP", "Windows 7", "Windows 10", "Symbian"},
		1200: {"Centos", "Ubuntu", "Windows 7", "Debain"}
	}
}