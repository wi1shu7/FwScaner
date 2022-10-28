#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import random
import sys
from config import entrance
from config import banner

if __name__ == '__main__':
    banner = random.choice(banner.banner)
    print(banner)

    modular = {
        "sub": "subdomain",
        "w": "whois",
        "r": "robots",
        "cms": "webcms",
        "bg": "webbg",
    }

    GO = {
        "subdomain": False,
        "whois": False,
        "robots": False,
        "webcms": False,
        "webbg": False,
    }
    parser = argparse.ArgumentParser(description='查看config目录下config.py文件更改配置', epilog="模块:subdomain(sub), whois(w), robots(r), webcms(cms), "
                                                                                     "webbg(bg)")
    pyVersion = float(sys.version[0:3])
    if pyVersion < 3.8:
        parser.add_argument('-u', '--url', help="输入要查询的url,可输入多个", nargs='*')
        parser.add_argument('-m', '--modular', help="选择的模块", nargs='*')
    else:
        parser.add_argument('-u', '--url', help="输入要查询的url,可输入多个", action='extend', nargs='*')
        parser.add_argument('-m', '--modular', help="要用的模块", action='extend', nargs='*')
    parser.add_argument('-a', '--all', help="启动全部模块", action='store_true')
    arg = parser.parse_args()

    try:
        if arg.all:
            for i in GO:
                GO[i] = True
        else:
            for i in arg.modular:
                if i in modular.keys():
                    i = modular[i]
                GO[i] = True
    except:
        print("[-] | 选择模块有误")
        parser.print_help()

    if GO["whois"]:
        print("------whoisRun------")
        entrance.whoisRun(arg.url)
    if GO["robots"]:
        print("------robotsRun------")
        entrance.robotsRun(arg.url)
    if GO["webbg"]:
        print("------webbackgroundRun------")
        entrance.webbackgroundRun(arg.url)
    if GO["subdomain"]:
        print("------subdomainRun------")
        entrance.subdomainRun(arg.url)
    if GO["webcms"]:
        print("------webcmsRun------")
        entrance.webcmsRun(arg.url)


