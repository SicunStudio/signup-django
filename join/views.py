from django.shortcuts import render
from join.models import People
from django.http import HttpResponse, Http404

import random

key = ''

def genRandStr(length):
    str = ''
    elementstr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for x in range(0, length):
        str = str + elementstr[random.randint(0,len(elementstr)-1)]
    return str


# Create your views here.
def index(request):
    return render(request, 'join/form.html', {'page_type': 'new'})


def submit_handler_add(request):
    if request.method == 'POST':
        existphone = People.objects.filter(phone=request.POST.get('phone'))
        existmail = People.objects.filter(mail=request.POST.get('mail'))
        if len(existphone) > 0 or len(existmail) > 0:
            return HttpResponse("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'><title>提交失败</title><link rel='stylesheet' href='/static/join/css/save_success.css'></head><body bgcolor='#ebeae5'><div id='body'><h3>填写的电话或邮箱已经报过名了</h3></div></body></html>")

        rname = request.POST.get('name')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')

        if rname == '' or phone == '' or mail == '':
            return HttpResponse("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'><title>提交失败</title><link rel='stylesheet' href='/static/join/css/save_success.css'></head><body bgcolor='#ebeae5'><div id='body'><h3>姓名、电话或邮箱为空</h3></div></body></html>")

        people = People()
        people.cid = genRandStr(16)
        people.name = request.POST.get('name')
        people.sex = request.POST.get('sex')
        people.classname = request.POST.get('classname')
        people.phone = request.POST.get('phone')
        people.qq = request.POST.get('qq')
        people.mail = request.POST.get('mail')

        people.depart1 = request.POST.get('depart1')
        people.depart2 = request.POST.get('depart2')
        if request.POST.get('adjustment')=='on':
            people.adjustment = True
        else:
            people.adjustment = False

        people.hobby = request.POST.get('hobby')
        people.experience = request.POST.get('experience')
        people.judge = request.POST.get('judge')
        people.save()

        return render(request, 'join/save_success.html')

    else:
        return Http404


def edit_index(request):
    return render(request, 'join/edit_login.html')


def edit_detail(request):
    if request.method == 'POST':
        people = People.objects.filter(name=request.POST.get('name'))
        people = people.filter(phone=request.POST.get('phone'))
        if len(people) == 1:
            return render(request, 'join/form.html', {'page_type': 'edit', 'data': people[0]})
        else:
            return HttpResponse("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'><title>错误</title><link rel='stylesheet' href='/static/join/css/save_success.css'></head><body bgcolor='#ebeae5'><div id='body'><h3>没有找到对应信息</h3></div></body></html>")


def edit_handler_save(request):
    if request.method == 'POST':
        people = People.objects.get(cid=request.POST.get('cid'))
        if people.name == request.POST.get('name') and people.phone == request.POST.get('phone'):
            people.sex = request.POST.get('sex')
            people.classname = request.POST.get('classname')
            people.qq = request.POST.get('qq')

            people.depart1 = request.POST.get('depart1')
            people.depart2 = request.POST.get('depart2')
            if request.POST.get('adjustment')=='on':
                people.adjustment = True
            else:
                people.adjustment = False

            people.hobby = request.POST.get('hobby')
            people.experience = request.POST.get('experience')
            people.judge = request.POST.get('judge')
            people.save()

        else:
            return Http404

        return render(request, 'join/save_success.html')

    else:
        return Http404
