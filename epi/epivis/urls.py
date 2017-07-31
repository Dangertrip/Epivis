from django.conf.urls import url
from . import views

app_name = 'epivis'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^menu', views.menu, name='menu'),
    url(r'^refresh_basemount', views.refresh_basemount, name='refresh_basemount'),
]
