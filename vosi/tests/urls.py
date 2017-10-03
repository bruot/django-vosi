from django.conf.urls import url, include

from vosi import views

urlpatterns = [
	url(r'^vosi/', include('vosi.urls', namespace='vosi')),
	url(r'^example1/', include('tests.urls_example1', namespace='example1')),
	url(r'^example2/', include('tests.urls_example2', namespace='example2')), #, app_name='example2'),
]
