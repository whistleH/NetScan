#coding:utf-8
from utils import *
import concurrent.futures
from urllib.parse import urljoin
import requests
from datetime import datetime
from config import DIR_DB, DIR_LOG
import base64

class DirScanner():
    def __init__(self, url, **kwargs):
        self._url = url
        self._scan_res = {}

        if 'thread_limit' in kwargs.keys():
            self._thread_limit = kwargs['thread_limit']
        else:
            self._thread_limit = 5

        if 'user-agent' in kwargs.keys():
            self._user_agent = kwargs['user-agent']
        else:
            self._user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0'

        self._log = DIR_LOG + "/" + base64.b64encode((url + "-" + str(datetime.now())).encode()).decode()
        self._fd = open(self._log,"w")
  
    def scanner(self, url):
        try:
            print(url)
            r = requests.get(
                url = url,
                headers={
                    'User-Agent':self._user_agent
                },
                timeout=2,
            )
            self._fd.write(str(r.status_code) + "," + url)
            # self._scan_res[url] = r.status_code
        except TimeoutError:
            self._fd.write(str(408) + "," + url)
        except:
            pass

    def start(self):
        path = []
        with open(DIR_DB + "/dicc.txt","r") as fin:
            path = fin.readlines()
        print("open the password")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._thread_limit) as executor:
            scan_res = [executor.submit(self.scanner, urljoin(self._url, router)) for router in path]
            [f.result() for f in scan_res] 
        
        return self._log

    def __del__(self):
        self._fd.close()
