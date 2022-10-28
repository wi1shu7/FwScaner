#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：pyj8thon -> 2
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2022/10/24 23:15
# @Software : win10 python3.6
import sys
import time
import os

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests as r
import argparse
from lxml import etree
import re
import gevent
from gevent import monkey;

monkey.patch_socket()
from gevent.pool import Pool
from gevent.queue import Queue
from gevent.lock import Semaphore

class subdomainCol:
    def __init__(self, domain, n, t, a, file, htp=False, uaheader=None, proxy=None, ):
        # 基础信息
        self.domain = domain
        self.n = n
        self.file = file
        # 存活和保存数据是否异步进行
        self.a = a
        self.lock = Semaphore(1)
        # 设置并发个数
        self.p = Pool(self.n)
        # 请求超时时间设置
        self.t = t
        # timeout = gevent.Timeout(int(self.t))
        # timeout.start()

        self.url = "https://www.dnsgrep.cn/subdomain/"
        self.sub_url = self.url + self.domain
        self.localUrl = "./output/" + self.domain + "/subdomain/"
        self.htp = htp
        # 设置代理
        if proxy is None:
            proxy = {"http":None,"https":None}
        self.proxy = proxy
        # 储存去重后的子域名
        self.fin_sub_domain = []
        # 储存验证存活的子域名
        self.subdomain = {}
        self.headers = {
            'authority': 'www.dnsgrep.cn',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        if uaheader is None:
            self.uaheader = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        else:
            self.uaheader = uaheader

    def collectSubdomain(self):
        # 发起请求
        if not self.file:  # 判断是否需要用字典
            try:
                request1 = r.get(self.sub_url, headers=self.headers)
                request1.encoding = "utf-8"
            except Exception as e:
                print("发起请求失败")
                print(e)
            # 处理结果
            try:
                sub_xpath = etree.HTML(request1.text)
                # 匹配结果数量
                num = sub_xpath.xpath(f'/html/body/article/div[2]/p/text()[2]')[0]
                sub_num = re.search('(\d+)条匹配结果', num)
                # 处理子域名
                self.processSubdomain(sub_xpath, num=sub_num.group(1))
            except Exception as e:
                print("运行失败")
                print(e)
        # 如果用字典,用这部分处理
        else:
            try:
                # 读取字典
                with open(self.file, "r") as f:
                    fstr = f.read()
                    flist = fstr.split("\n")
                # 处理子域名
                self.processSubdomain(flist, mode=True)
            except Exception as e:
                print("运行失败")
                print(e)

        # 添加输出文件夹
        if not os.path.exists(r'./output/' + self.domain + "/subdomain/"):
            os.makedirs(r'./output/' + self.domain + "/subdomain/")

        print("[+] |--------" + self.domain + "--------")
        print("[+] | subdomain  |  statusCode\n[+] |-----------------------------")
        # 验活
        # 验证子域名存活
        self.siteSur_start()
        # 保存数据，异步已经保存不用这步
        if not self.a:
            self.saveData()

        subTime = time.ctime()

        print("_____" + subTime + "_____\n")
        for i in self.subdomain:
            with open(self.localUrl + i + ".txt", "a") as f:
                f.write("_____" + self.domain + "_____\n")
            with open(self.localUrl + i + ".txt", "a") as f:
                f.write("_____" + subTime + "_____\n")

    # 处理子域名,mode为判断是否用字典
    def processSubdomain(self, subX, num=0, mode=False, ):
        try:
            sub = []
            if not mode:
                for i in range(2, int(num) + 2):
                    # 匹配子域名url
                    j = subX.xpath(f"/html/body/article/div[2]/table/tr[{str(i)}]/td[1]/text()")[0]
                    # 处理子域名url，然后加入列表
                    j = j.replace("\n", "").replace(" ", "")
                    if j != "":
                        sub.append(j)
            else:
                for i in subX:
                    if i != "":
                        sub.append(i + "." + self.domain)
            # 去重
            self.delRepetition(sub)
        except Exception as e:
            print("处理子域名失败")
            print(e)

    # 去重
    def delRepetition(self, sub):
        try:
            # 集合去重
            p = set()
            for i in sub:
                p.add(i)
            self.fin_sub_domain = list(p)
            self.fin_sub_domain.append(self.domain)
            # print(self.fin_sub_domain)
        except Exception as e:
            print("去重失败")
            print(e)

    # 验证是否存活
    def siteSur_start(self):
        try:
            subQueue = Queue()
            t = [self.p.spawn(self.siteSur, i, subQueue, self.proxy, self.uaheader, self.htp) for i in self.fin_sub_domain]
            gevent.joinall(t)
            # j用于记录状态码
            j = []
            self.writeSubdomain(subQueue, j)
        except Exception as e:
            print("error:siteSur_start")
            print(e)

    # 请求子域名判断是否存活
    def siteSur(self, sub, subQueue, proxy, uaheader, htp):

        url = "http://" + sub
        urls = "https://" + sub
        headers = {
            "User-Agent": uaheader,
        }
        reqq = ""
        # 发起请求
        if htp:
            try:
                reqq = r.get(urls, headers=headers, timeout=self.t, verify=False, proxies=proxy)
            except Exception:
                pass
        else:
            try:
                reqq = r.get(url, headers=headers, timeout=self.t, proxies=proxy)
            except Exception:
                pass

        # 处理数据
        if reqq != "":
            code = str(reqq.status_code)
            if reqq.status_code >= 400:
                print("[-] | " + sub + " " + code)
            else:
                print("[+] | " + sub + " " + code)
            subQueue.put([code, sub])
            # 判断是否异步，异步保存数据
            if self.a:
                # self.lock.acquire()
                with open(self.localUrl + code + ".txt", "ab", buffering=0) as f:
                    f.write(sub.encode("utf-8") + b"\n")
                # self.lock.release()
        else:
            print("[-] | " + sub + " connect fail")
            with open(self.localUrl + "connect_fail" + ".txt", "ab", buffering=0) as f:
                f.write(sub.encode("utf-8") + b"\n")

    # 数据写入到subdomain字典
    def writeSubdomain(self, subQueue, j):
        try:
            while not subQueue.empty():
                i = subQueue.get()
                if i[0] not in j:
                    self.subdomain[i[0]] = []
                    j.append(i[0])
                self.subdomain[i[0]].append(i[1])
        except Exception as e:
            print("error:writeSubdomain")
            print(e)

    # 保存数据
    def saveData(self):
        try:
            for code, i in self.subdomain.items():
                with open(self.localUrl + code + ".txt", "a") as f:
                    for j in i:
                        f.write(j + "\n")
        except Exception as e:
            print("error:saveData")
            print(e)


def formatUrlDict(urlfile):
    with open(urlfile, "r", encoding="utf-8") as f:
        fp = f.read()
        furl = fp.split("\n")
    return furl

if __name__ == '__main__':
    banner = '''
            _       _             _              
 __ __ __  (_)     / |     ___   | |_     _  _   
 \ V  V /  | |     | |    (_-<   | ' \   | +| |  
  \_/\_/  _|_|_   _|_|_   /__/_  |_||_|   \_,_|  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
-----------------------------------------------------
    '''
    print(banner + "\n")

    # 命令行接受url
    parser = argparse.ArgumentParser(description="A subdomain name collector(摆烂的)",
                                     epilog='happy every day',
                                     conflict_handler='resolve',
                                     # exit_on_error=False,
                                     )
    try:
        pyVersion = float(sys.version[0:3])
        if pyVersion < 3.8:
            parser.add_argument('-u', '--url', help="输入要查询的url，可输入多个", nargs='*')
        else:
            parser.add_argument('-u', '--url', help="输入要查询的url，可输入多个", action='extend', nargs='*')
        parser.add_argument('-n', help="线程数,默认5", default=5, type=int)
        parser.add_argument('-t', '--timeout', help="超时秒数,默认3", default=3, type=int)
        parser.add_argument('-a', help="验证存活和保存数据是否异步进行，默认False", action='store_true')
        parser.add_argument('-f', '--file',
                            help="使用字典,指定字典的路径，默认为不使用字典，数据从www.dnsgrep.cn/subdomain爬取",
                            default=False)
        parser.add_argument('--urlfile', help="读取文件里的url探测子域名,指定字典的路径", action="store_true")
        parser.add_argument('--http', help="是否启用https,默认不启用", action="store_true")
        domain = parser.parse_args()
    except Exception as e:
        print(e)
        parser.print_help()

    # 查询子域名
    # 判断读取的是否是字典
    if not domain.urlfile:
        for i in domain.url:
            A = subdomainCol(i.rstrip("/"), domain.n, domain.timeout, domain.a, domain.file, htp=domain.http)
            A.collectSubdomain()
    else:
        furl = formatUrlDict(domain.urlfile)
        for i in furl:
            A = subdomainCol(i.rstrip("/"), domain.n, domain.timeout, domain.a, domain.file, htp=domain.http)
            A.collectSubdomain()


def subdomainGo(domainList, n, timeout, a, file, htp, uaheader, porxy):
    for i in domainList:
        A = subdomainCol(i.rstrip("/"), n, timeout, a, file, htp=htp, uaheader=uaheader, proxy=porxy)
        A.collectSubdomain()