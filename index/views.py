from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index/index.html')

def intro_index(request):
    return render(request, 'index/intro/index.html')