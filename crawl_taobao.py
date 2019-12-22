# coding=utf-8
import re
import urllib.request
import urllib


def crawl_taobao():
    # 淘宝上搜索的关键词
    key = "比基尼"
    key = urllib.request.quote(key)
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    # 分页爬取
    for i in range(0, 4):
        url = "https://s.taobao.com/search?q=" + key
        data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        pat = 'data-src="//(.*?)"'
        imagelist = re.compile(pat, re.S).findall(data)
        # 爬取每一页中所有的图片
        for j in range(0, len(imagelist)):
            thisimg = imagelist[j]
            thisimgurl = "http://" + thisimg
            # 保存到自己电脑的D盘
            savefile = 'D:/pic/' + str(i) + str(j) + '.jpg'
            urllib.urlretrieve(thisimgurl, savefile)



if __name__ == '__main__':
    crawl_taobao()

