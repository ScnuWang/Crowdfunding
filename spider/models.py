from django.utils import timezone
from django.db import models
# 产品
class TaoBaoProject(models.Model):
    project_name = models.CharField(max_length=255)
    original_id = models.CharField(max_length=255,unique=True)
    curr_money = models.DecimalField(max_digits=18,decimal_places=2)
    target_money = models.DecimalField(max_digits=18,decimal_places=2)
    # 众筹成功：1；众筹中：2；众筹失败：3；众筹异常：4
    status = models.CharField(max_length=255)
    status_value = models.IntegerField()
    project_url = models.CharField(max_length=255)
    finish_per = models.IntegerField()
    support_person = models.IntegerField()
    focus_count = models.IntegerField()
    video_url = models.CharField(max_length=255)
    qrcode = models.CharField(max_length=255)
    project_image = models.CharField(max_length=255)
    remain_day = models.IntegerField()
    person_name = models.CharField(max_length=255)
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    update_time = models.DateTimeField(default=timezone.now().strftime('%Y-%m-%d 12:00:00'))

# 产品支持项
class TaoBaoprojectItem(models.Model):
    title  = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    # 这里数据库默认使用关联对象的主键,如果是其他字段，需要设置to_field ,并且关联对象的对应字段设置unique=True
    project = models.ForeignKey(TaoBaoProject,on_delete=models.CASCADE,to_field='original_id')
    image = models.CharField(max_length=255)
    # max_digits：数据总长，decimal_places，小数点位数
    price = models.DecimalField(max_digits=18,decimal_places=2)
    support_person = models.IntegerField()
    total = models.IntegerField()
    desc = models.CharField(max_length=255)
    update_time = models.DateTimeField(default=timezone.now().strftime('%Y-%m-%d 12:00:00'))


class CrawlTask(models.Model):
    # 产品原始编号
    project_original_id = models.CharField(max_length=255)
    # 产品抓取地址
    project_crawl_url = models.CharField(max_length=255)
    # 网站编号 (淘宝：1)
    website_id = models.IntegerField()
    # 抓取状态 （初始化：1，抓取成功：2，抓取失败：3,抓取异常：4,初始化完成：5；抓取完成：6）
    crawl_status = models.IntegerField(default=1)
    # 抓取次数
    crawl_count = models.IntegerField(default=1)
    # 抓取时间
    crawl_time = models.DateTimeField(default=timezone.now().strftime('%Y-%m-%d 12:00:00'))
    # 最后一次抓取时间
    last_crawl_time = models.DateTimeField(auto_now=True)
