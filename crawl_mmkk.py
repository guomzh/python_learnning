# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 2019-12-22 不得不说，Python这短短的100多行代码，设计到网络编程、正则表达式、字符串处理 知识点，让我爬取到大量
# 高质量的美女图片，让我对其中涉及的更深入的计网、爬虫等知识原理产生兴趣

"""
图片(文件)下载,核心方法是 urllib.request 模块的 urlretrieve()方法
 urlretrieve(url, filename=None, reporthook=None, data=None)
 url: 文件url
 filename: 保存到本地时,使用的文件(路径)名称
 reporthook: 文件传输时的回调函数
 data: post提交到服务器的数据
 该方法返回一个二元元组("本地文件路径",<http.client.HTTPMessage对象>)
"""
import socket
import urllib.request
import time
import os
import requests
from lxml import etree

headers = {
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

# 设置超时时间为3s
socket.setdefaulttimeout(3)
log_folder = ''


def crawl(key_name):
    url = 'https://www.mmkk.me/search/{k}/'.format(k=key_name)

    # headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0")

    # java中为 yyy-MM-dd HH:mm:ss  python中为 %Y-%m-%d %H:%M:%S
    current_time = time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))
    folder = 'D:/2019/爬虫图片/{t}'.format(t=key+current_time)
    log_folder = folder + '/log'
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.makedirs(log_folder)
    count = 1
    for i in range(9, 21):
        one_search_folder = folder + '/' + str(i)
        one_search_url = url + str(i) + '/'
        if not os.path.exists(one_search_folder):
            os.makedirs(one_search_folder)
        else:
            print('dir {d} exist'.format(d=one_search_url))
        try:
            crawl_begin(one_search_folder, one_search_url)
        except:
            print("crawl函数，  异常出现： {times} 次, 此时当前目录: {f}, 当前url： {u}".format(times=count, f=one_search_folder,
                                                                              u=one_search_url))
            count += 1
            continue


def crawl_begin(folder, url):
    html = request_get(url)

    # //ul[@class="ali"]//a/img/@src
    img_titles = html.xpath('//div[@class="item-title"]//a//div/text()')
    img_urls = html.xpath('//div[@class="item-title"]//a//@href')
    data = zip(img_titles, img_urls)
    for img_title, img_url in data:
        print('开始搜索{title}'.format(title=img_title))
        # img_url = 'https:' + img_url
        img_url = img_url.replace('\n', '').replace('\t', '')
        folder_name = '{f}/{title}'.format(f=folder, title=img_title).replace('\n', '').replace('\t', '')
        special_crawl(folder_name, img_url)


def special_crawl(folder, url):
    if not os.path.exists(folder):
        os.makedirs(folder)
    html = request_get(url)

    # //ul[@class="ali"]//a/img/@src
    img_titles = html.xpath('//div[@data-fancybox="gallery"]//img//@title')
    img_urls = html.xpath('//div[@data-fancybox="gallery"]//img//@data-original')
    data = zip(img_titles, img_urls)
    for img_title, img_url in data:
        print('开始下载{title}.jpg'.format(title=img_title))
        # img_url = 'https:' + img_url
        img_url = img_url.replace('\n', '').replace('\t', '')
        print(img_url)
        file_name = '{f}/{title}.jpg'.format(f=folder, title=img_title).replace('\n', '').replace('\t', '')
        try:
            result = urllib.request.urlretrieve(img_url,
                                                filename=file_name,
                                                reporthook=None,
                                                data=None)
            # print(result)
        except socket.timeout:
            count = 1
            while count <= 5:
                try:
                    urllib.request.urlretrieve(img_url,
                                               filename=file_name,
                                               reporthook=None,
                                               data=None)
                    break
                except socket.timeout:
                    count += 1
            if count > 5:
                print("special_crawl 下载具体图片Url: {pic} failed!".format(pic=img_url))


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


def request_get(url):
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            resp.encoding = 'UTF-8'
        html = etree.HTML(resp.text)
        return html
    except:
        count = 1
        while count <= 5:
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    resp.encoding = 'UTF-8'
                html = etree.HTML(resp.text)
                return html
                break
            except:
                count += 1
        if count > 5:
            print("requests.get函数，   异常出现： {times} 次".format(times=count))


if __name__ == '__main__':
    key = '美女'
    crawl(key)
    print('爬取 ({k}) 图片结束！'.format(k=key))

