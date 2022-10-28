#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：pyj8thon -> webbackground
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2022/10/27 2:09
# @Software : win10 python3.6
import os
import random
import sys

import requests as r

import gevent
from gevent.pool import Pool
from gevent.queue import Queue
from gevent.lock import Semaphore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class backgroundCol():
    def __init__(self, urlList, n, timeout, htp=True, fileUrl=None, allow_redirects=False, proxy=None, uaheader=None):
        self.urlList = urlList
        # 设置字典路径
        if fileUrl is None:
            if sys.path[0][-4:] == 'util':
                fileUrl = "../static/bg_url_dict.txt"
            else:
                fileUrl = './static/bg_url_dict.txt'
        self.fileUrl = fileUrl
        # 设置线程数
        self.p = Pool(n)
        # 设置超时时间
        self.t = timeout
        # 设置代理
        if proxy is None:
            proxy = {"http":None,"https":None}
        self.proxy = proxy
        # 设置UA头
        if uaheader is None:
            uaheader = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            ]
        self.uaheader = uaheader
        # http or https
        if htp:
            self.htp = 'https://'
        else:
            self.htp = 'http://'
        self.allow_red = allow_redirects
        self.urlQueue = Queue()
        self.lock = Semaphore(1)


    def start(self):

        for url in self.urlList:
            url = url.rstrip("/")
            # 判断文件夹是否存在
            if not os.path.exists('./output/' + url + "/background/"):
                os.makedirs('./output/' + url + "/background/")

            self.readFileUrl()
            print("[+] |--------" + url + "--------")
            print("[+] |    url    |   statusCode\n[ ] |-----------------------------")
            while not self.urlQueue.empty():
                header = {
                    'user-agent': random.choice(self.uaheader)
                }
                t = self.p.spawn(self.scanBackground, url, self.urlQueue.get(), self.t, self.htp, allow_red=self.allow_red, proxy=self.proxy, uaheader=header)
            gevent.joinall([t])

    def readFileUrl(self):
        with open(self.fileUrl, 'r') as f:
            flist = f.read().split("\n")
        for i in flist:
            self.urlQueue.put(i)

    def scanBackground(self, url, bgUrl, t, htp, allow_red, proxy, uaheader):
        reUrl = htp + url + bgUrl
        saveUrl = './output/' + url + "/background/"
        req = ""
        if htp == 'https://':
            try:
                req = r.get(reUrl, headers=uaheader, timeout=t, proxies=proxy, verify=False, allow_redirects=allow_red)
            except:
                pass
        else:
            try:
                req = r.get(reUrl, headers=uaheader, timeout=t, proxies=proxy, allow_redirects=allow_red)
            except:
                pass

        if req != "":
            code = str(req.status_code)
            if req.status_code < 400:
                print("[+] | " + reUrl + " : " + code)
            else:
                print("[-] | " + reUrl + " : " + code)
            self.saveBackground(saveUrl, reUrl, code)
        else:
            print("[-] | " + reUrl + " : connect fail")
            self.saveBackground(saveUrl, reUrl, 'connect_fail')

    def saveBackground(self, saveUrl, reUrl, code):
        # self.lock.acquire()
        with open(saveUrl + code + ".txt", "ab", buffering=0) as f:
            f.write(reUrl.encode("utf-8") + b"\n")
        # self.lock.release()

def webbackgroundGo(urlList, n, timeout, htp, fileUrl, allow_redirects, proxy, uaheader):
    A = backgroundCol(urlList, n, timeout, htp=htp, fileUrl=fileUrl, allow_redirects=allow_redirects, proxy=proxy, uaheader=uaheader)
    A.start()