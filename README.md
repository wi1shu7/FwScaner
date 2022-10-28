# FwScaner

## 说明

应该有点用的工具，FwScaner是一款收集CMS、WHOIS 、DNS、robots.txt、子域名的工具。

查看config目录下config.py文件更改配置

（小孩子不懂事写着玩的

## 环境

>python 3.7+ (小于3.7的版本没用过
>
>linux or windows

## 目录结构

```
"""
. 目录结构 :
├── firstRun.py(第一次使用或config文件缺失时可运行)
├── welcome.py(启动函数)  Start function
├── requirements.txt(依赖库) Dependent library
├── config（配置文件） Profile
│   ├── config.py(参数配置) Parameter configuration
│   ├── entrance.py(入口函数) Entry function
│   └── banner.py(banner) banner
├── output(输出目录) Output directory
│   ├── url1 (域名1) 
│   │   ├──background (后台扫描信息) Scan background information
│   │   ├──subdomain (子域名信息) Subdomain information
│   │   ├──whois (whois信息) Whois information
│   │   └──robots.txt (robots信息) Robots information
│   ├── url2 (域名2) 
│   │   ├──background (后台扫描信息) Scan background information
│   │   ├──subdomain (子域名信息) Subdomain information
│   │   ├──whois (whois信息) Whois information
│   │   └──robots.txt (robots信息) Robots information
├── static(静态资源目录) Static resource directory
│   ├── bg_url_dict.txt (默认后台扫描字典) Default Background Scan Dictionary
│   └── cmsData.json (cms指纹信息) CMS fingerprint information
├── util(功能函数目录)  Function function directory
│   ├── formatUrlDict.py 处理字典数据
│   ├── robots.py 获取robots.txt文件
│   ├── subdomain.py 获取子域名数据
│   ├── webbackground 后台扫描
│   ├── webcms.py cms识别
│   └── whois.py whois查询
└── README.md(说明文档) Documentation
"""
```

## 用法

`python welcome.py [-h] [-u [URL [URL ...]]] [-m [MODULAR [MODULAR ...]]] [-a]`

- `-h -help` 帮助信息

- `-u --url` 输入要查询的url,可输入多个

- `-a -all` 选择全部模块

- `-m --modular` 选择的模块

  参数有：

  - subdomain (sub) ——子域名
  - whois (w) ——whois信息
  - robots (r) ——robots.txt
  - webcms (cms) ——cms
  - webbg (bg) ——扫描后台

## Help information

```
usage: welcome.py [-h] [-u [URL [URL ...]]] [-m [MODULAR [MODULAR ...]]] [-a]

查看config目录下config.py文件更改配置

optional arguments:
  -h, --help            show this help message and exit
  -u [URL [URL ...]], --url [URL [URL ...]]
                        输入要查询的url，可输入多个
  -m [MODULAR [MODULAR ...]], --modular [MODULAR [MODULAR ...]]
                        要用的模块
  -a, --all             启动全部模块,不包括ascanner模块

模块:subdomain(sub), whois(w), robots(r), webcms(cms), webbg(bg)
```

