from django.shortcuts import render
from join.models import People
from docxtpl import DocxTemplate
import os, os.path
import random
import signup.settings
from django.utils.http import urlquote

from django.http import StreamingHttpResponse, Http404, HttpResponse


def genRandStr(length):
    str = ''
    elementstr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for x in range(0, length):
        str = str + elementstr[random.randint(0,len(elementstr)-1)]
    return str


# Create your views here.
def list_index(request):
    people = People.objects.all()
    return render(request, 'control/list/list.html', {'data': people})


def generate_docx_handler(request):
    if request.method == 'POST':
        people = People.objects.get(cid=request.POST.get('cid'))
        tploc = os.path.join(signup.settings.BASE_DIR, 'docx\\tmplte.docx')
        doc = DocxTemplate(tploc)
        adjustment = '否'
        if people.adjustment:
            adjustment = '是'
        context = {'name': people.name, 'sex': people.sex, 'classname': people.classname, 'phone': people.phone, 'qq': people.qq, 'mail': people.mail, 'depart1': people.depart1, 'depart2': people.depart2, 'adjustment': adjustment, 'hobby': people.hobby, 'experience': people.experience, 'judge': people.judge}
        doc.render(context)
        genfile = os.path.join(signup.settings.BASE_DIR, 'temp\\'+genRandStr(12)+'.docx')
        doc.save(os.path.join(genfile))

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

        target_file_name = people.name + ' - ' + people.phone + '.docx'
        target_file_name = urlquote(target_file_name)

        response = StreamingHttpResponse(file_iterator(genfile))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="'+target_file_name+'"'
        # os.remove(genfile)
        return response

    else:
        return Http404
