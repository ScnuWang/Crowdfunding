from django.test import TestCase
import requests
# Create your tests here.
from datetime import datetime
import time

if __name__ == '__main__':

    project_crawl_url = 'https://izhongchou.taobao.com/dream/ajax/getProjectForDetail.htm?id=20078369'
    response = requests.get(project_crawl_url).json()['data']
    for item in response['items']:
        print(item)
    # print(datetime.strftime(response['begin_date']),'%Y-%m-%d %H:%M:%S')