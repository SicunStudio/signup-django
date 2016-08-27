from django.shortcuts import render
from control import views

# Create your views here.
def index(request):
    return render(request, 'templates/index')