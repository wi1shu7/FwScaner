#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：pyj8thon -> robot         
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2022/10/27 13:14
# @Software : win10 python3.6
import os

import requests as r
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import gevent
from gevent.pool import Pool
from gevent.lock import Semaphore
lock = Semaphore(1)

def robotsCol(url, timeout, proxy=None, uaheader=None):
    global lock
    if proxy is None:
        proxy = {"http": None, "https": None}
    if uaheader is None:
        uaheader = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    headers = {
        'user-agent': uaheader,
    }

    req = None
    reqs = None
    try:
        req = r.get("http://" + url + "/robots.txt", headers=headers, timeout=timeout, proxies=proxy)
    except:
        pass

    try:
        reqs = r.get("https://" + url + "/robots.txt", headers=headers, timeout=timeout, verify=False, proxies=proxy)
    except:
        pass

    if not os.path.exists('./output/' + url + '/'):
        os.makedirs('./output/' + url + '/')

    if reqs is not None:
        if reqs.status_code == 200:
            lock.acquire()
            with open('./output/' + url + '/robots.txt', "a") as f:
                f.write("\n-----https://" + url + "/robots.txt-----\n")
                f.write(reqs.text)
                lock.release()
                print("http://" + url + "/robots.txt已保存到" + './output/' + url + '/robots.txt下\n')

    if req is not None:
        if req.status_code == 200:
            lock.acquire()
            with open('./output/' + url + '/robots.txt', "a") as f:
                f.write("\n-----http://" + url + "/robots.txt-----\n")
                f.write(req.text)
                lock.release()
                print("https://" + url + "/robots.txt已保存到" + './output/' + url + '/robots.txt下\n')

    if req is None and reqs is None:
        print("未找到robots.txt文件")
    elif req is not None and req.status_code > 200:
        print("http://" + url + "/robots.txt : " + str(req.status_code))
    elif reqs is not None and reqs.status_code > 200:
        print("https://" + url + "/robots.txt : " + str(reqs.status_code))


def robotsGo(urlList, n, timeout, uaheader, proxy):
    p = Pool(n)
    t = [p.spawn(robotsCol, url, timeout, proxy=proxy, uaheader=uaheader) for url in urlList]
    gevent.joinall(t)
