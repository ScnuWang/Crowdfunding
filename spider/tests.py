from django.test import TestCase
import requests
# Create your tests here.
from datetime import datetime
import time
import urllib
import json
import html
import re

if __name__ == '__main__':

    # tb_project_crawl_url = 'https://izhongchou.taobao.com/dream/ajax/getProjectForDetail.htm?id=20078369'
    id = str(10052647)
    project_crawl_url = 'https://izhongchou.taobao.com/dream/ajax/getProjectForDetail.htm?id=' + id
    # response = requests.get(project_crawl_url).json()['data']  #这样直接提取会报错
    response = requests.get(project_crawl_url).text
    # print(response)
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", response)
    result = json.loads(fixed)['data']
    print(result)

    # xm_project_list = 'https://home.mi.com/app/shopv3/pipe'
    # ================小米测试
    # xm_project = 'https://youpin.mi.com/app/shop/pipe'
    # headers= {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.8',
    #             'content-type': 'application/x-www-form-urlencoded',
    #             'Referer': '//home.mi.com/crowdfundinglist?id=78&title=%E4%BC%97%E7%AD%B9',
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # gid = 207
    # detailparm = "{\"detail\":{\"model\":\"Shopv2\",\"action\":\"getDetail\",\"parameters\":{\"gid\":\"%s\"}},\"comment\":{\"model\":\"Comment\",\"action\":\"getList\",\"parameters\":{\"goods_id\":\"%s\",\"orderby\":\"1\",\"pageindex\":\"0\",\"pagesize\":3}},\"activity\":{\"model\":\"Activity\",\"action\":\"getAct\",\"parameters\":{\"gid\":\"%s\"}}}" % (gid, gid, gid)
    # detailreq = urllib.parse.quote(detailparm)
    # detailreq = "data=" + detailreq
    # response = requests.post(xm_project, data=detailreq, headers=headers)
    # print(response.json()['result']['detail']['data'])