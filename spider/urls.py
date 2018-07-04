from django.urls import path
from . import views
urlpatterns = [
    path('crawl_manage', views.crawl_manage,name='crawl_manage'),
]