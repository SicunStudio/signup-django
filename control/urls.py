from django.conf.urls import url
from control import views


urlpatterns = [
    url(r'^/list$', views.list_index, name='list_index'),

    url(r'^/handler/file', views.generate_docx_handler, name='download_word'),
]