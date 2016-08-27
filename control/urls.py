from django.conf.urls import url
from control import views


urlpatterns = [
    url(r'^/list$', views.list_index, name='list_index'),
]