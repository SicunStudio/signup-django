from django.shortcuts import render
from join.models import People
from control.models import Config

import os, os.path
import random
import signup.settings
from django.utils.http import urlquote

from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponse, HttpResponseRedirect

from docxtpl import DocxTemplate
from zipfile import ZipFile

import datetime

import shutil

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def genRandStr(length):
    str = ''
    elementstr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for x in range(0, length):
        str = str + elementstr[random.randint(0,len(elementstr)-1)]
    return str


def login_index(request):
    return render(request, 'control/login/login.html')


def login_handler(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/control/list')
        else:
            return HttpResponseRedirect('/control/login')
    else:
        return HttpResponseNotFound("<h2>Page Not Found</h2>")


@login_required(login_url='/control/login')
def logout_handler(request):
    logout(request)
    return HttpResponseRedirect('/control/list')


@login_required(login_url='/control/login')
def list_index(request):
    config_ifopen = Config.objects.filter(name='ifopen')
    config_ifopen_value = 'no'
    if len(config_ifopen) == 0:
        ifopen = Config()
        ifopen.name = 'ifopen'
        ifopen.value = 'no'
        ifopen.save()
    else:
        config_ifopen_value = config_ifopen[0].value

    people = People.objects.all()
    return render(request, 'control/list/list.html', {'data': people, 'ifopen': config_ifopen_value})


### folder：生成的临时文件放在temp目录下的folder子目录
### 注意：folder不为空时，文件夹生成之后不会自动删除
### 返回值：生成的文件在服务器上的路径
def generate_docx(cid, filename, folder=''):
    people = People.objects.get(cid=cid)
    tploc = os.path.join(signup.settings.BASE_DIR, 'docx\\tmplte.docx')
    doc = DocxTemplate(tploc)
    adjustment = '否'
    if people.adjustment:
        adjustment = '是'
    context = {'name': people.name, 'sex': people.sex, 'classname': people.classname, 'phone': people.phone,
               'qq': people.qq, 'mail': people.mail, 'depart1': people.depart1, 'depart2': people.depart2,
               'adjustment': adjustment, 'hobby': people.hobby, 'experience': people.experience, 'judge': people.judge}
    doc.render(context)
    folder_path = os.path.join(signup.settings.BASE_DIR, 'temp', folder)
    if folder != '':
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        genfile_uri = 'temp\\' + folder + '\\' + filename + '.docx'
    else:
        genfile_uri = 'temp\\' + filename + '.docx'
    genfile = os.path.join(signup.settings.BASE_DIR, genfile_uri)
    doc.save(os.path.join(genfile))
    return genfile


@login_required(login_url='/control/login')
def generate_docx_handler(request):
    if request.method == 'POST':
        people = People.objects.get(cid=request.POST.get('cid'))
        genfile = generate_docx(request.POST.get('cid'), genRandStr(12))

        #发起文件下载
        def file_iterator(file_name, chunk_size=128):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
            f.close()
            if os.path.exists(file_name):
                os.remove(file_name)

        target_file_name = people.depart1 + ' - ' + people.name + ' - ' + people.phone + '.docx'
        target_file_name = urlquote(target_file_name)

        response = StreamingHttpResponse(file_iterator(genfile))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="'+target_file_name+'"'
        return response

    else:
        return HttpResponseNotFound("<h2>Page Not Found</h2>")


@login_required(login_url='/control/login')
def generate_zip_handler(request):
    if request.method == 'POST':
        folder_name = genRandStr(8)
        peoples = People.objects.all()
        folder_path = os.path.join(signup.settings.BASE_DIR, 'temp', folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        zipfileloc = os.path.join(folder_path, genRandStr(10) + '.zip')
        with ZipFile(zipfileloc, 'w') as zippack:
            for people in peoples:
                docx_name = people.depart1 + ' - ' + people.name + ' - ' + people.phone
                genfile = generate_docx(people.cid, docx_name, folder_name)
                zippack.write(genfile, people.depart1 + "\\" + docx_name + '.docx')
            # 关闭zip写入
            zippack.close()

        # 发起下载
        def file_iterator(file_name, chunk_size=128):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
            f.close()
            #删除临时文件夹
            if os.path.exists(file_name):
                shutil.rmtree(os.path.dirname(file_name))

        target_file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.zip'
        target_file_name = urlquote(target_file_name)

        response = StreamingHttpResponse(file_iterator(zipfileloc))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="' + target_file_name + '"'
        return response

    else:
        return HttpResponseNotFound("<h2>Page Not Found</h2>")


@login_required(login_url='/control/login')
def receive_form_on(request):
    config_ifopen = Config.objects.filter(name='ifopen')
    if len(config_ifopen) == 0:
        ifopen = Config()
        ifopen.name = 'ifopen'
        ifopen.value = 'yes'
        ifopen.save()
    else:
        config_ifopen[0].value = 'yes'
        config_ifopen[0].save()

    return HttpResponseRedirect('/control/list')


@login_required(login_url='/control/login')
def receive_form_off(request):
    config_ifopen = Config.objects.filter(name='ifopen')
    if len(config_ifopen) == 0:
        ifopen = Config()
        ifopen.name = 'ifopen'
        ifopen.value = 'no'
        ifopen.save()
    else:
        config_ifopen[0].value = 'no'
        config_ifopen[0].save()
    return HttpResponseRedirect('/control/list')

