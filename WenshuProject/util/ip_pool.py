#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import platform
import requests
import time
import redis

pl = platform.system()

if pl == "Linux":
    redis_obj = redis.Redis(host='127.0.0.1', port=6379, db=4)
else:
    redis_obj = redis.Redis(host='master', port=6379, db=4)


def get_proxies_from_xun_youzhi():
    ip_pool = []
    url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=bee3b5cbacef42f89f861130ed898e71&orderno=YZ201810192048oyA1Wm&returnType=2&count=10"
    res = requests.get(url=url)
    jsondata = json.loads(res.text)
    ips = jsondata['RESULT']
    print(ips)
    if ips:
        for ip in ips:
            host = ip["ip"]
            port = ip["port"]
            proxy = "http://" + host + ":" + port
            proxies = {"https": proxy, "http": proxy}
            ip_pool.append(proxies)
    return ip_pool


def get_proxies_from_sun():
    """
    提取太阳代理的函数
    :return:
    """
    ip_pool = []
    url = "http://http.tiqu.qingjuhe.cn/getip?num=10&type=2&pro=&city=0&yys=0&port=1&pack=22871&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=0&regions="
    res = requests.get(url=url)
    jsondata = json.loads(res.text)
    print(jsondata)
    # if jsondata["success"]=="True":
    #     print("提取太阳代理成功!!!")
    ips = jsondata['data']
    if ips:
        print("提取太阳代理success")
        for ip in ips:
            host = ip["ip"]
            extime = ip['expire_time']
            ts = int(time.mktime(time.strptime(extime, "%Y-%m-%d %H:%M:%S")))
            vtime = ts - int(time.time() - 20)
            port = ip["port"]
            print(host + ":" + str(port))
            proxy = "http://" + host + ":" + str(port)
            proxies = {"https": proxy, "http": proxy}
            redis_obj.sadd(proxies, proxies)
            redis_obj.expire(proxies, vtime)
    else:
        raise ValueError("太阳代理已经提取完毕改成提取讯代理......")


def get_xun_proxies():
    ips = get_proxies_from_xun_youzhi()
    for proxies in ips:
        # 设置过期时间
        redis_obj.sadd(proxies, proxies)
        redis_obj.expire(proxies, 180)


def start():
    try:
        get_proxies_from_sun()
    except Exception as err:
        get_xun_proxies()


if __name__ == "__main__":
    start()
