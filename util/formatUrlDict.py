#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：pyj8thon -> formatUrlDict         
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2022/10/27 14:17
# @Software : win10 python3.6

def formatUrlDict(urlfile):
    with open(urlfile, "r", encoding="utf-8") as f:
        fp = f.read()
        furl = fp.split("\n")
    return furl