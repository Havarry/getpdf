#!/usr/bin/env python
# -*- coding : UTF-8 -*-
import http
import random
import socket

import pandas as pd
import requests
import time


header = {
        'Host': 'query.sse.com.cn',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
    }


def get_proxy_ip():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = "HJPC87609J7D516D"
    proxyPass = "26D9C5391F9123CA"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


# 获取pdf内容
def get_content(purl):
    while True:
        try:
            timeout = random.choice(range(80, 180))
            proxy = get_proxy_ip()
            req = requests.post(purl, headers=header, timeout=timeout, proxies=proxy, stream=True)
            req.encoding = 'GBK'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(2, 5)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(2, 6)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(3, 5)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(2, 4)))
    # NOTE the stream=True parameter
    return req.iter_content(chunk_size=1024)


# 将内容写入到本地pdf
def write_to_pdf(content):
    with open('pdf.pdf', 'wb') as f:
        for chunk in content:  # 1024 是一个比较随意的数，表示分几个片段传输数据。
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()  # 刷新也很重要，实时保证一点点的写入。


def get_code():
    path = '股票代码.xlsx'
    all_data = pd.read_excel(path, converters={u'证券代码': str})
    codes = all_data.get('证券代码')  # 证券代码
    return codes


def get_nianbao_url(stkcd):
    random_num = str(random.randint(10000, 99999))
    code = stkcd
    begin_year = '2002'
    end_year = '2004'
    req_time = str(time.time())
    url = 'http://query.sse.com.cn/security/stock/queryCompanyStatementNew.do?jsonCallBack=jsonpCallback'+random_num + \
          '&isPagination=true&productId=' + code + '&keyWord=&isNew=1&reportType2=DQBG&reportType=YEARLY&beginDate=' + \
          begin_year + '-01-01&endDate=' + end_year + '-01-01&pageHelp.pageSize=25&pageHelp.pageCount=50' + \
          '&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=' + req_time
    return url


if __name__ == '__main__':
    codes = get_code()
    for code in codes:
        url = get_nianbao_url(code)
        print(url)
        # break
    # pdf_url = 'http://static.sse.com.cn/disclosure/listedinfo/announcement/c/2017-03-25/601999_2016_n.pdf'
    # print(pdf_url)
    # write_to_pdf(get_content(pdf_url))


