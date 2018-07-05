from datetime import datetime
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import JsonResponse
from .models import CrawlTask
from .taobao import crawl_tb_init,crawl_tb
from .xiaomi import crawl_xm_init,crawl_xm

def crawl_manage(request):
    # 多线程


    tb_init_task = CrawlTask.objects.filter(crawl_status=5,website_id=1, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    xm_init_task = CrawlTask.objects.filter(crawl_status=5,website_id=2, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    if not list(tb_init_task):
        crawl_tb_init()
    if not list(xm_init_task):
        crawl_xm_init()

    tb_crawl_task = CrawlTask.objects.filter(crawl_status=6,website_id=1, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    xm_crawl_task = CrawlTask.objects.filter(crawl_status=6,website_id=2, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    if not list(tb_crawl_task):
        crawl_tb()
    if not list(xm_crawl_task):
        crawl_xm()

    if CrawlTask.objects.filter(crawl_status=6, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00')):
        return JsonResponse({'status': 'SUCCESS'})

    return JsonResponse({'status': 'FAILED'})