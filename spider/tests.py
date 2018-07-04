from django.test import TestCase
import requests
# Create your tests here.
from datetime import datetime
import time
import urllib
if __name__ == '__main__':

    # tb_project_crawl_url = 'https://izhongchou.taobao.com/dream/ajax/getProjectForDetail.htm?id=20078369'
    # xm_project_list = 'https://home.mi.com/app/shopv3/pipe'
    xm_project = 'https://youpin.mi.com/app/shop/pipe'
    headers= {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'Referer': '//home.mi.com/crowdfundinglist?id=78&title=%E4%BC%97%E7%AD%B9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # param = 'data=%7B%22detail%22%3A%7B%22model%22%3A%22Shopv2%22%2C%22action%22%3A%22getDetail%22%2C%22parameters%22%3A%7B%22gid%22%3A%22102505%22%7D%7D%2C%22comment%22%3A%7B%22model%22%3A%22Comment%22%2C%22action%22%3A%22getList%22%2C%22parameters%22%3A%7B%22goods_id%22%3A%22102505%22%2C%22orderby%22%3A%221%22%2C%22pageindex%22%3A%220%22%2C%22pagesize%22%3A3%7D%7D%2C%22activity%22%3A%7B%22model%22%3A%22Activity%22%2C%22action%22%3A%22getAct%22%2C%22parameters%22%3A%7B%22gid%22%3A%22102505%22%7D%7D%7D'
    # response = requests.post(xm_project,params=param,headers=headers)
    # print(response.json())

    gid = 102505
    detailparm = "{\"detail\":{\"model\":\"Shopv2\",\"action\":\"getDetail\",\"parameters\":{\"gid\":\"%s\"}},\"comment\":{\"model\":\"Comment\",\"action\":\"getList\",\"parameters\":{\"goods_id\":\"%s\",\"orderby\":\"1\",\"pageindex\":\"0\",\"pagesize\":3}},\"activity\":{\"model\":\"Activity\",\"action\":\"getAct\",\"parameters\":{\"gid\":\"%s\"}}}" % (gid, gid, gid)
    detailreq = urllib.parse.quote(detailparm)
    detailreq = "data=" + detailreq
    response = requests.post(xm_project, data=detailreq, headers=headers)
    print(response.json()['result']['detail']['data']['good']['name'])