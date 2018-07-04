from datetime import datetime
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import JsonResponse
from .models import CrawlTask
from .taobao import crawl_tb_init,crawl_tb

def crawl_manage(request):
    init_task = CrawlTask.objects.filter(crawl_status=5, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    # 多线程怎么办???


    if not list(init_task):
        crawl_tb_init()

    crawl_task = CrawlTask.objects.filter(crawl_status=6, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    if not list(crawl_task):
        crawl_tb()

    if CrawlTask.objects.filter(crawl_status=6, crawl_time__gte=datetime.now().strftime('%Y-%m-%d 00:00:00')):
        return JsonResponse({'status': 'SUCCESS'})

    return JsonResponse({'status': 'FAILED'})