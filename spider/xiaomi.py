import urllib
from datetime import datetime
from django.utils import timezone
import requests
from .models import XiaoMiProject,XiaoMiProjectItem,CrawlTask

# 获取要抓取的项目列表，并
def crawl_tb_init():
    projectList_Url = 'https://home.mi.com/app/shopv3/pipe'
    headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.8',
               'content-type': 'application/x-www-form-urlencoded',
               'Referer': '//home.mi.com/crowdfundinglist?id=78&title=%E4%BC%97%E7%AD%B9',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    param = 'data=%7B%22request%22%3A%7B%22model%22%3A%22Homepage%22%2C%22action%22%3A%22BuildHome%22%2C%22parameters%22%3A%7B%22id%22%3A%2278%22%7D%7D%7D'

    projects = requests.post(projectList_Url,params=param,headers=headers).json()['result']['request']['data']

    for project in projects:
        original_id = project['gid']
        project_crawl_url = 'https://youpin.mi.com/app/shop/pipe'
        crawltask = CrawlTask()
        crawltask.project_original_id = original_id
        crawltask.project_crawl_url = project_crawl_url
        crawltask.website_id = 1
        crawltask.save()

    crawltask = CrawlTask()
    crawltask.crawl_status = 5
    crawltask.website_id = 1
    crawltask.save()
    return


def crawl_tb():
    tasklist = CrawlTask.objects.filter(website_id=1,crawl_status__in=(1,4))
    project_url_prefix = 'https://izhongchou.taobao.com/dreamdetail.htm?id='
    for task in tasklist:
        try:
            # 获取每个详细信息的数据
            headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'content-type': 'application/x-www-form-urlencoded',
                       'Referer': '//home.mi.com/crowdfundinglist?id=78&title=%E4%BC%97%E7%AD%B9',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            gid = task.project_original_id
            detailparm = "{\"detail\":{\"model\":\"Shopv2\",\"action\":\"getDetail\",\"parameters\":{\"gid\":\"%s\"}},\"comment\":{\"model\":\"Comment\",\"action\":\"getList\",\"parameters\":{\"goods_id\":\"%s\",\"orderby\":\"1\",\"pageindex\":\"0\",\"pagesize\":3}},\"activity\":{\"model\":\"Activity\",\"action\":\"getAct\",\"parameters\":{\"gid\":\"%s\"}}}" % (
            gid, gid, gid)
            detailreq = urllib.parse.quote(detailparm)
            detailreq = "data=" + detailreq
            response = requests.post(task.project_crawl_url, data=detailreq, headers=headers).json()['result']['detail']['data']

            # 保存数据
            project = XiaoMiProject()
            project.original_id = task.project_original_id
            good_response = response['good']
            project.project_name = good_response['name']
            project.curr_money = good_response['saled_fee']
            project.target_money = good_response['target_money']

            status_value = int(response['status_value'])

            if status_value in [6,8,9,]:
                project.status = '众筹成功'
                project.status_value = 1
            elif status_value in [4,]:
                project.status = '众筹中'
                project.status_value = 2
            #     完整百分比小于100 并且 剩余天数为0
            elif int(response['finish_per']) < 100 and response['remain_day'] == 0:
                project.status = '众筹失败'
                project.status_value = 3
            else:
                project.status = '众筹异常'
                project.status_value = 4

            project.project_url = project_url_prefix + project.original_id
            project.finish_per = response['finish_per']
            project.support_person = response['support_person']
            project.focus_count = response['focus_count']
            project.video_url = response['video']
            project.qrcode = response['qrcode']
            project.project_image = response['image']
            project.remain_day = response['remain_day']
            project.person_name = response['nick']
            begin_date = response['begin_date']
            end_date = response['end_date']
            if begin_date:
                project.begin_date = datetime.strptime(response['begin_date'], '%Y/%m/%d').strftime('%Y-%m-%d 00:00:00')
            else:
                project.begin_date = timezone.now().strftime('%Y-%m-%d 00:00:00')
            if end_date:
                project.end_date = datetime.strptime(response['end_date'], '%Y/%m/%d').strftime('%Y-%m-%d 00:00:00')
            else:
                project.begin_date = timezone.now().strftime('%Y-%m-%d 00:00:00')

            project.save()

            # 支持档
            for item in response['items']:
                project_item = XiaoMiProjectItem()
                project_item.title = item['title']
                project_item.item_id = item['item_id']
                project_item.project_id = project.original_id
                project_item.image = item['images']
                project_item.price = item['price']
                project_item.support_person = item['support_person']
                project_item.total = item['total']
                project_item.desc = item['desc']
                project_item.save()

            # 修改task状态
            task.crawl_status = 2
            task.save()
        except Exception as error:
            print(error)
            # 如果是第一次抓取异常，再抓取一次，抓取次数多余2次，设置为抓取失败
            if task.crawl_count == 1:
                task.crawl_status = 4
                task.crawl_count += 1
            else:
                task.crawl_status = 3
                task.crawl_count += 1
        continue
    crawltask = CrawlTask()
    crawltask.crawl_status = 6
    crawltask.website_id = 1
    crawltask.save()
    return