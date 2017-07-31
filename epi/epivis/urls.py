from django.conf.urls import url
from . import views

app_name = 'epivis'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^menu', views.menu, name='menu'),
    url(r'^refresh_basemount', views.refresh_basemount, name='refresh_basemount'),
    url(r'^show_files',views.show_files_page,name='show_files'),
    url(r'^get_files_info',views.get_files_info,name='get_files_info'),
]
