from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index/index.html')


def intro_index(request):
    return render(request, 'index/intro/index.html')


def intro_depart(request, depart):
    deplist = ['cw', 'gx', 'ms', 'mt', 'rl', 'sc', 'st', 'wl', 'wq', 'wy', 'xc', 'xm', 'xz']
    if depart in deplist:
        return render(request, 'index/intro/depart/'+depart+'.html')
    else:
        return HttpResponse("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'><title>提交失败</title><link rel='stylesheet' href='/static/join/css/save_success.css'></head><body bgcolor='#ebeae5'><div id='body'><h3>地址错了，请返回上一页</h3></div></body></html>")