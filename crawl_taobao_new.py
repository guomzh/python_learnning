# !/usr/bin/env python
# -*- coding:utf-8 -*-


"""
图片(文件)下载,核心方法是 urllib.urlrequest 模块的 urlretrieve()方法
 urlretrieve(url, filename=None, reporthook=None, data=None)
 url: 文件url
 filename: 保存到本地时,使用的文件(路径)名称
 reporthook: 文件传输时的回调函数
 data: post提交到服务器的数据
 该方法返回一个二元元组("本地文件路径",<http.client.HTTPMessage对象>)
"""

import urllib.request
import time
import os
import requests
from lxml import etree


def crawl():
    key = '比基尼'
    url = 'https://s.taobao.com/search?q={k}'.format(k=key)
    headers = {
        # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    }
    # headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0")

    # java中为 yyy-MM-dd HH:mm:ss  python中为 %Y-%m-%d %H:%M:%S
    current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    folder = 'D:/图片下载爬虫/{t}'.format(t=key+current_time)
    if not os.path.exists(folder):
        os.makedirs(folder)
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
    html = etree.HTML(resp.text)

    # //ul[@class="ali"]//a/img/@src
    img_titles = html.xpath('//div[@class="pic"]//a/img/@alt')
    img_urls = html.xpath('//div[@class="pic"]//a/img/@data-src')
    data = zip(img_titles, img_urls)
    for img_title, img_url in data:
        print('开始下载{title}.jpg'.format(title=img_title))
        img_url = 'https:' + img_url
        result = urllib.request.urlretrieve(img_url,
                                            filename='{dir}/{title}.jpg'.format(dir=folder, title=img_title),
                                            reporthook=loading,
                                            data=None)
        # print(result)


def loading(blocknum, blocksize, totalsize):
    """
    回调函数: 数据传输时自动调用
    blocknum:已经传输的数据块数目
    blocksize:每个数据块字节
    totalsize:总字节
    """
    percent = int(100 * blocknum * blocksize / totalsize)
    if percent > 100:
        percent = 100
    print("正在下载>>>{}%".format(percent))
    import time
    time.sleep(0.5)


if __name__ == '__main__':
    crawl()

