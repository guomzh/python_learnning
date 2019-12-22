# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import urllib.request
from lxml import etree


def crawl():
    url = 'http://www.ivsky.com/tupian/haiyangshijie/'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    }

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
    html = etree.HTML(resp.text)

    img_titles = html.xpath('//ul[@class="ali"]//a/@title')
    img_urls = html.xpath('//ul[@class="ali"]//a/img/@src')


    data = zip(img_titles, img_urls)
    for img_title, img_url in data:
        print('开始下载{title}.jpg'.format(title=img_title))
        img_url = 'https:' + img_url
        result = urllib.request.urlretrieve(img_url,
                                            filename='D:/图片下载爬虫/{title}.jpg'.format(title=img_title),
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