from django.conf.urls import url, include
from vosi import views

app_name = 'example2'

urlpatterns = [
    url(r'^availability/$', views.availability, name='availability'),
    url(r'^capabilities/$', views.capabilities, name='capabilities'),
]