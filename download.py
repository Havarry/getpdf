#!/usr/bin/env python
# -*- coding : UTF-8 -*-
import random

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


# 获取pdf内容
def get_content(purl):
    time.sleep(0.5)  # 限制下载的频次速度，以免被封
    # NOTE the stream=True parameter
    r = requests.post(purl, stream=True)
    return r.iter_content(chunk_size=1024)


# 将内容写入到本地pdf
def write_to_pdf(content):
    with open('pdf.pdf', 'wb') as f:
        for chunk in content:  # 1024 是一个比较随意的数，表示分几个片段传输数据。
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()  # 刷新也很重要，实时保证一点点的写入。


def get_code():
    pass


def get_nianbao_url():
    random_num = str(random.randint(10000, 99999))
    code = ''
    begin_year = ''
    end_year = ''
    req_time = str(time.time())
    url = 'http://query.sse.com.cn/security/stock/queryCompanyStatementNew.do?jsonCallBack=jsonpCallback'+random_num + \
          '&isPagination=true&productId=' + code + '&keyWord=&isNew=1&reportType2=DQBG&reportType=YEARLY&beginDate=' + \
          begin_year + '-01-01&endDate=' + end_year + '-01-01&pageHelp.pageSize=25&pageHelp.pageCount=50' + \
          '&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=' + req_time


if __name__ == '__main__':
    pdf_url = 'http://static.sse.com.cn/disclosure/listedinfo/announcement/c/2017-03-25/601999_2016_n.pdf'
    write_to_pdf(get_content(pdf_url))

