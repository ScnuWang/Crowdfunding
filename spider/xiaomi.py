import urllib
from datetime import datetime
from django.utils import timezone
import requests
from .models import XiaoMiProject,XiaoMiProjectItem,CrawlTask

# 获取要抓取的项目列表，并
def crawl_xm_init():
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
        crawltask.website_id = 2
        crawltask.save()

    crawltask = CrawlTask()
    crawltask.crawl_status = 5
    crawltask.website_id = 2
    crawltask.save()
    return


def crawl_xm():
    tasklist = CrawlTask.objects.filter(website_id=2,crawl_status__in=(1,4))
    project_url_prefix = 'https://youpin.mi.com/detail?gid='
    for task in tasklist:
        project = XiaoMiProject()
        try:
            # 获取每个详细信息的数据
            headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'content-type': 'application/x-www-form-urlencoded',
                       'Referer': '//home.mi.com/crowdfundinglist?id=78&title=%E4%BC%97%E7%AD%B9',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            gid = task.project_original_id
            detailparm = "{\"detail\":{\"model\":\"Shopv2\",\"action\":\"getDetail\",\"parameters\":{\"gid\":\"%s\"}},\"comment\":{\"model\":\"Comment\",\"action\":\"getList\",\"parameters\":{\"goods_id\":\"%s\",\"orderby\":\"1\",\"pageindex\":\"0\",\"pagesize\":3}},\"activity\":{\"model\":\"Activity\",\"action\":\"getAct\",\"parameters\":{\"gid\":\"%s\"}}}" % (gid, gid, gid)
            detailreq = urllib.parse.quote(detailparm)
            detailreq = "data=" + detailreq
            response = requests.post(task.project_crawl_url, data=detailreq, headers=headers).json()['result']['detail']['data']

            # 保存数据
            project.original_id = task.project_original_id

            good_response = response['good']
            crowdfunding_reaponse = good_response['crowdfunding']

            project.project_name = good_response['name']
            project.curr_money = float(good_response['saled_fee'])*0.01
            project.target_money = good_response['saled']

            finish_per = int(crowdfunding_reaponse['flag_percent'])
            begin_date = int(crowdfunding_reaponse['start'])
            end_date = int(crowdfunding_reaponse['end'])

            if begin_date:
                project.begin_date = datetime.fromtimestamp(begin_date)
            else:
                project.begin_date = timezone.now().strftime('%Y-%m-%d 00:00:00')
            if end_date:
                project.end_date = datetime.fromtimestamp(end_date)
            else:
                project.begin_date = timezone.now().strftime('%Y-%m-%d 00:00:00')


            if datetime.now().timestamp() < end_date and crowdfunding_reaponse['flag_name'] == '筹款中':
                project.status = '众筹中'
                project.status_value = 2
            elif finish_per > 100 or crowdfunding_reaponse['flag_name'] == '成功':
                project.status = '众筹成功'
                project.status_value = 1
            #     完整百分比小于100 并且 剩余天数为0
            elif finish_per < 100 and datetime.now().timestamp() > end_date:
                project.status = '众筹失败'
                project.status_value = 3
            else:
                project.status = '众筹异常'
                project.status_value = 4

            project.project_url = project_url_prefix + project.original_id
            project.finish_per = finish_per
            project.support_person = good_response['saled']
            project.focus_count = 0
            project.video_url = ''
            project.qrcode = ''
            project.project_image = good_response['pic_url']
            if end_date > int(datetime.now().timestamp()):
                project.remain_day = int((end_date-int(datetime.now().timestamp()))/(60*60*24))
            else:
                project.remain_day = 0
            # 早期项目不存在这个字段
            try:
                project.person_name = response['brand']['merchant_name']
            except:
                project.person_name = ''

            # 保存至数据库
            project.save()

            # 支持档
            for item in response['props']:
                project_item = XiaoMiProjectItem()
                project_item.title = item['name']
                project_item.item_id = item['pid']
                project_item.project_id = project.original_id
                project_item.image = item['img']
                project_item.price = float(item['price'])*0.01
                project_item.support_person = item['saled']
                project_item.total = item['total_limit']
                project_item.desc = item['summary']
                project_item.save()

            # 修改task状态
            task.crawl_status = 2
            task.save()
        #     处理int('')错误的问题
        except ValueError as  error:
            print('===> 原始编号',task.project_original_id,'------------》 平台编号',task.website_id,'------------',error)
        except Exception as error:
            print('===> 原始编号',task.project_original_id,'------------》 平台编号',task.website_id,'-------------',error)
            # 如果是第一次抓取异常，再抓取一次，抓取次数多余2次，设置为抓取失败
            if task.crawl_count == 1:
                task.crawl_status = 4
                task.crawl_count += 1
            else:
                task.crawl_status = 3
                task.crawl_count += 1
            task.save()

    crawltask = CrawlTask()
    crawltask.crawl_status = 6
    crawltask.website_id = 2
    crawltask.save()
    return