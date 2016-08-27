from django.shortcuts import render
from join.models import People


# Create your views here.
def list_index(request):
    people = People.objects.all()
    return render(request, 'control/list/list.html', {'data': people})
