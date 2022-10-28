import argparse
import json
import os
import sys
import time

import requests as r
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import gevent
from gevent import monkey;

monkey.patch_socket()
from gevent.pool import Pool
from gevent.lock import Semaphore


class whoisCol:
    def __init__(self, domain, n, t):
        self.domainList = domain
        # 设置超时数
        self.t = t
        # 设置线程数
        self.n = n
        self.p = Pool(int(self.n))
        # 设置锁
        self.whoisPrint = Semaphore(1)

    def start(self):
        t = [self.p.spawn(self.collectWhois, i.rstrip("/"), self.t) for i in self.domainList]
        gevent.joinall(t)

    def formatData(self, domain, whoisDict):
        self.whoisPrint.acquire()
        print("\n[ ] | _____" + domain + "_____")
        if whoisDict["status"] == "True":
            for j, k in whoisDict.items():
                print("[+] | " + j + " : " + k)
        else:
            for j, k in whoisDict.items():
                print("[-] | " + j + " : " + k)
        print("数据已保存到" + './output/' + domain + "/whois/" + domain + ".txt下\n")
        self.whoisPrint.release()

    def collectWhois(self, domain, t):
        # 设置请求参数和超时时间
        t = int(t)
        url = "https://api.devopsclub.cn/api/whoisquery"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52"
        }
        params = {
            "domain": domain,
            "type": "json",
        }
        # 设置存储路径
        localUrl = './output/' + domain + "/whois/"
        # 请求数据
        try:
            req = r.get(url, params=params, headers=headers, verify=False, timeout=t)
            reqJson = json.loads(req.text)
            # print(reqJson)
            # 添加输出文件夹
            if not os.path.exists(localUrl):
                os.makedirs(localUrl)
            # 存储数据
            whoisDict = {}
            # 处理数据
            self.processWhois(domain, reqJson, whoisDict)
            # 保存数据
            self.saveData(domain, whoisDict, localUrl)
            # 输出数据
            self.formatData(domain, whoisDict)
        except Exception as e:
            print("error:collectWhois")
            print(e)

    def processWhois(self, domain, reqJson, whoisDict):
        status = reqJson['data']['status']
        data = reqJson["data"]["data"]
        # 判断请求状态
        if status == 0:
            # 说明状态
            whoisDict.update({"status": "True"})
            dataName = {
                "creationDate": "创建日期",
                "contactEmail": "联系人电子邮件",
                "contactPhone": "联系电话",
                "nameServer": "dnsNameServer",
                "domainName": "域名",
                "domainStatus": "域名状态",
                "expirationTime": "到期时间",
                "registrant": "注册人",
                "registrar": "注册商",
                "registrarWHOISServer": "registrarWHOISServer",
                "registrationTime": "登记时间",
                "updatedDate": "更新日期",
                "registrarAbuseContactEmail": "注册人联系电子邮件",
                "registrarAbuseContactPhone": "注册人联系电话",
                "registrarIANAID": "注册人IANAID",
                "registrarURL": "注册地址",
                "registryDomainID": "注册域名ID",
                "registryExpiryDate": "注册到期日期",
                "registrantContactEmail": "注册联系人邮件"
            }
            for i in data:
                str1 = ""
                # 判断值是否是一个列表
                if type(data[i]).__name__ == "list":
                    for j in data[i]:
                        str1 += j + ", "
                else:
                    str1 = data[i]
                if i in dataName:
                    whoisDict.update({dataName[i]: str1})
                else:
                    whoisDict.update({i: str1})

        else:
            # # 说明状态
            whoisDict.update({"status": "False"})
            statusNum = {
                '1': '域名解析失败',
                '2': '域名未注册',
                '3': '暂不支持此域名后缀查询',
                '4': '域名查询失败',
                '5': '请求数据错误',
            }
            whoisDict.update({"false": statusNum[str(status)],
                              "msg": reqJson["msg"],
                              })

    def saveData(self, domain, whoisDict, localUrl):
        with open(localUrl + domain + ".txt", "a") as f:
            f.write("\n_____" + time.ctime() + "_____\n")
        for j, k in whoisDict.items():
            with open(localUrl + domain + ".txt", "ab") as f:
                f.write((j + " : " + k).encode("utf-8") + b"\n")


if __name__ == '__main__':
    banner = """
 ▄█     █▄   ▄█     ▄████████    ▄█    █▄    ███    █▄  
███     ███ ███    ███    ███   ███    ███   ███    ███ 
███     ███ ███▌   ███    █▀    ███    ███   ███    ███ 
███     ███ ███▌   ███         ▄███▄▄▄▄███▄▄ ███    ███ 
███     ███ ███▌ ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ 
███     ███ ███           ███   ███    ███   ███    ███ 
███ ▄█▄ ███ ███     ▄█    ███   ███    ███   ███    ███ 
 ▀███▀███▀  █▀    ▄████████▀    ███    █▀    ████████▀  

"""
    print(banner)
    parser = argparse.ArgumentParser(description="A whois collector(摆烂的)",
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
        parser.add_argument('-n', help="线程数,默认5", default="5")
        parser.add_argument('-t', '--timeout', help="超时秒数,默认7", default="7")
        parser.add_argument('--urlfile', help="读取文件里的url探测子域名,指定字典的路径", default=False)
        domain = parser.parse_args()

        if len(domain.url) == 0 and not domain.urlfile:
            print("请输入url,用参数-u或--urlfile")
            parser.print_help()
        else:
            if not domain.urlfile:
                urlList = domain.url
            else:
                with open(domain.urlfile, "r") as f:
                    urlList = f.read().split("\n")

            A = whoisCol(urlList, domain.n, domain.timeout, )
            A.start()
    except Exception as e:
        # print(e)
        parser.print_help()


def whoisGo(urlList, n, timeout, ):
    A = whoisCol(urlList, n, timeout, )
    A.start()
