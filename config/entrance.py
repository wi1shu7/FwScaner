from config import config
from util import subdomain
from util import whois
from util import robots
from util import formatUrlDict
from util import webcms
from util import webbackground
import random


def subdomainRun(domainList):
    n = config.subdomain["NUMTHREADS"]
    timeout = config.subdomain["TIMEOUT"]
    a = config.subdomain["ASYNCHRONOUS"]
    file = config.subdomain["DICTURL"]
    urlfile = config.subdomain["URLFILE"]
    htp = config.subdomain["HTTP"]
    proxy = config.proxies
    uaheader = random.choice(config.USER_AGENTS)
    if urlfile:
        domainList = formatUrlDict(urlfile)
    subdomain.subdomainGo(domainList, n, timeout, a, file, htp, uaheader, proxy)


def whoisRun(domainList):
    n = config.whois["NUMTHREADS"]
    timeout = config.whois["TIMEOUT"]
    urlfile = config.whois["URLFILE"]
    if urlfile:
        domainList = formatUrlDict(urlfile)
    whois.whoisGo(domainList, n, timeout, )


def robotsRun(domainList):
    n = config.robots["NUMTHREADS"]
    timeout = config.robots["TIMEOUT"]
    urlfile = config.robots["URLFILE"]
    proxy = config.proxies
    uaheader = random.choice(config.USER_AGENTS)
    if urlfile:
        domainList = formatUrlDict(urlfile)
    robots.robotsGo(domainList, n, timeout, uaheader, proxy)


def webcmsRun(domainList):
    n = config.webcms["NUMTHREADS"]
    timeout = config.webcms["TIMEOUT"]
    urlfile = config.webcms["URLFILE"]
    htp = config.webcms["HTTP"]
    proxy = config.proxies
    uaheader = config.USER_AGENTS
    if urlfile:
        domainList = formatUrlDict(urlfile)
    webcms.webcmsGo(domainList, n, timeout, htp, uaheader, proxy)


def webbackgroundRun(domainList):
    n = config.webbackground["NUMTHREADS"]
    timeout = config.webbackground["TIMEOUT"]
    urlfile = config.webbackground["URLFILE"]
    htp = config.webbackground["HTTP"]
    dicturl = config.webbackground["DICTURL"]
    allow_redirects = config.webbackground["ALLOWREDIRECTS"]
    proxy = config.proxies
    uaheader = config.USER_AGENTS
    if urlfile:
        domainList = formatUrlDict(urlfile)
    webbackground.webbackgroundGo(domainList, n, timeout, htp, dicturl, allow_redirects, proxy, uaheader)