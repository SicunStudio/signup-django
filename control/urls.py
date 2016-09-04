from django.conf.urls import url
from control import views


urlpatterns = [
    url(r'^$', views.list_index),
    url(r'^/login$', views.login_index, name='login_index'),
    url(r'^/handler/login$', views.login_handler, name='login_handler'),
    url(r'^/handler/logout$', views.logout_handler, name='logout_handler'),

    url(r'^/list$', views.list_index, name='list_index'),

    url(r'^/handler/file$', views.generate_docx_handler, name='download_word'),

    url(r'^/handler/file/zip', views.generate_zip_handler, name='download_zip'),

    url(r'^/handler/open/on', views.receive_form_on, name='receive_on_handler'),
    url(r'^/handler/open/off', views.receive_form_off, name='receive_off_handler'),
]