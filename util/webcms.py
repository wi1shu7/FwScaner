#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：pyj8thon -> webcms
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2022/10/27 2:03
# @Software : win10 python3.6
import os
import random
import traceback

import requests as r
import json, hashlib, sys
import gevent
from gevent.pool import Pool
from gevent import monkey;

monkey.patch_socket()
from gevent.queue import Queue
from gevent.lock import Semaphore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class cmsCol:
    def __init__(self, urlList, n, timeout, htp=False, proxy=None, uaheader=None):
        # 设置线程数
        self.p = Pool(n)
        # 设置请求超时时间
        self.t = timeout
        #
        self.htp = htp
        # 设置请求头
        if uaheader is None:
            self.header = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", ]
        else:
            self.header = uaheader
        # 设置代理
        if proxy is None:
            proxy = {"http": None, "https": None}
        self.proxy = proxy
        # 设置锁
        self.lock = Semaphore(1)
        # 判断是否识别出cms
        self.status = False
        self.data = Queue()
        self.urlList = urlList

    def start(self):

        for url in self.urlList:
            url = url.rstrip("/")
            # 判断文件夹是否存在
            if not os.path.exists('./output/' + url + "/"):
                os.makedirs('./output/' + url + "/")

            print("[ ] |----- " + url + " -----")
            self.cmsData()
            while not self.data.empty():
                headers = {
                    'user-agent': random.choice(self.header),
                }
                t = self.p.spawn(self.scanCms, url, self.data.get(), self.t, self.htp, headers, self.proxy)
            gevent.joinall([t])
            if not self.status:
                print("[-] | CMS: " + url + "未识别出")

    def cmsData(self):
        if sys.path[0][-4:] != "util":
            with open('./static/cmsData.json', 'r', encoding="utf-8") as f:
                fjson = json.load(f)
            for i in fjson:
                self.data.put(i)

    def clearQueue(self):
        while not self.data.empty():
            self.data.get()

    def cmsMd5(self, text):
        m = hashlib.md5()
        m.update(text.encode("utf8"))
        return m.hexdigest()

    def scanCms(self, url, cmsInfo, t, htp, header, proxy):
        url1 = "http://" + url + cmsInfo["url"]
        url2 = "https://" + url + cmsInfo["url"]
        # 发起请求
        print_url = ""
        req = ''
        if htp:
            try:

                req = r.get(url2, headers=header, timeout=t, proxies=proxy)
                print_url = url1
            except Exception:
                pass
        else:
            try:

                req = r.get(url1, headers=header, timeout=t, verify=False, proxies=proxy)
                print_url = url2
            except Exception:
                pass

        try:
            judge = False
            if req == "":
                judge = True
            if req.status_code != 200:
                judge = True
            rtext = req.text
            if rtext is None:
                judge = True
            if judge:
                print("[-] |  CMS is not " + cmsInfo["name"])
                return None
        except:
            rtext = ''

        if cmsInfo["re"]:
            if (rtext.find(cmsInfo["re"]) != -1):
                result = cmsInfo["name"]
                print("[+] | CMS:%s Judge:%s re:%s" % (result, print_url, cmsInfo["re"]))
                self.clearQueue()
                self.lock.acquire()
                self.status = True
                self.lock.release()
                return True
        else:
            md5 = self.cmsMd5(rtext)
            if md5 == cmsInfo["md5"]:
                result = cmsInfo["name"]
                print("[+] | CMS:%s Judge:%s md5:%s" % (result, print_url, cmsInfo["md5"]))
                self.clearQueue()
                self.lock.acquire()
                self.status = True
                self.lock.release()
                return True


def webcmsGo(urlList, n, timeout, htp, uaheader, proxy):
    A = cmsCol(urlList, n, timeout, htp=htp, proxy=proxy, uaheader=uaheader)
    A.start()
