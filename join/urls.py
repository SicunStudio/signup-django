from django.conf.urls import url
from join import views

urlpatterns = [
    url(r'^$', views.index, name='join_submit'),

    url(r'^/handler/add', views.submit_handler_add, name='handler_submit_add'),

    url(r'^/edit$', views.edit_index, name='edit_index'),
    url(r'^/edit/detail', views.edit_detail, name='edit_handler'),
    url(r'^/handler/edit', views.edit_handler_save, name='handler_edit_save'),
]