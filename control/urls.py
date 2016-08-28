from django.conf.urls import url
from control import views


urlpatterns = [
    url(r'^$', views.list_index),
    url(r'^/login$', views.login_index, name='login_index'),
    url(r'^/handler/login$', views.login_handler, name='login_handler'),
    url(r'^/handler/logout$', views.logout_handler, name='logout_handler'),

    url(r'^/list$', views.list_index, name='list_index'),

    url(r'^/handler/file', views.generate_docx_handler, name='download_word'),
]