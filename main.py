# python 学习总结
# 1、basic_func 基本类型
# 2、字符串操作
#
#
#
#
#
#
import time

import requests

headers = {
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}


def basic_func():
    # 数字
    a = 5
    # 字符串
    b = 'string: I am python'
    # map
    c = {'name :': 'map', 'age ：': 23, 'state :': 'single'}
    # list
    d = [12, 'list', b, c]
    # tuple
    e = (12, 'tuple', b, c)
    # set
    f = {3, 3, 4, 5, 5, b, b}
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)


def string_func():
    a = 'python'
    b = a + 'is funny.'
    print(b)
    print(b[3])
    c = b[3:5]
    print(c)


def for_func():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    for i in range(0, 4):
        print(i)


def test_request_timeout():
    try:
        # - timeout = ([连接超时时间], [读取超时时间])
        resp = requests.get("https://www.guomzho.com", headers=headers, timeout=5)
    except:
        print('request 出现异常，测试成功')


if __name__ == "__main__":
    # basic_func()
    # string_func()
    # for_func()
    test_request_timeout()

