from django.conf.urls import url, include
from . import views

app_name = 'vosi'

urlpatterns = [
    # vosi endpoints required by dali: capabilities, availability
    # the general view functions will list all capabilities, for DAL-specific
    # capabilities, please map in your app's url to different view functions
    url(r'^availability/$', views.availability, name='availability'),
    url(r'^capabilities/$', views.capabilities, name='capabilities'),
]