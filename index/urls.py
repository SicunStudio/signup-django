from django.conf.urls import url
from index import views

urlpatterns = [
    url(r'^intro', views.intro_index, name='intro_index'),
    url(r'^', views.index, name='index'),
]