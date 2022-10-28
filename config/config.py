# 模块配置
# -------------------------------------------------------------------------------------
subdomain = {

    # 线程数
    "NUMTHREADS": 100,
    # 请求超时时间
    "TIMEOUT": 3,
    # 读取文件里的url探测子域名,指定字典的路径
    "URLFILE": False,
    # 验证存活和保存数据是否异步进行
    "ASYNCHRONOUS": True,
    # 是否启用https
    "HTTP": True,
    # 使用字典,指定字典的路径，默认为不使用字典，数据从www.dnsgrep.cn/subdomain爬取
    "DICTURL": False
}

whois = {

    # 线程数
    "NUMTHREADS": 5,
    # 请求超时秒数
    "TIMEOUT": 7,
    # 读取文件里的url探测子域名,指定字典的路径
    "URLFILE": False
}

robots = {

    # 线程数
    "NUMTHREADS": 5,
    # 请求超时秒数
    "TIMEOUT": 3,
    # 读取文件里的url探测子域名,指定字典的路径
    "URLFILE": False
}

webcms = {

    # 线程数
    "NUMTHREADS": 100,
    # 请求超时秒数
    "TIMEOUT": 2,
    # 是否启用https
    "HTTP": True,
    # 读取文件里的url探测子域名,指定字典的路径
    "URLFILE": False
}

webbackground = {

    # 线程数
    "NUMTHREADS": 100,
    # 请求超时秒数
    "TIMEOUT": 1,
    # 读取文件里的url探测子域名,指定字典的路径
    "URLFILE": False,
    # 是否启用https
    "HTTP": True,
    # 是否允许重定向
    "ALLOWREDIRECTS": False,
    # 扫描所用字典,指定路径
    "DICTURL": "./static/bg_url_dict.txt"
}
# -------------------------------------------------------------------------------------


# 设置请求代理(包含subdomain, robots, webbackground, webcms模块
proxies = {
    "http": None,
    "https": None
}

# user-agent
USER_AGENTS = [

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    "Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; "
    "Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322;"
    " .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0;"
    " .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2;"
    " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727;"
    " InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3)"
    " Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    "Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",

]
