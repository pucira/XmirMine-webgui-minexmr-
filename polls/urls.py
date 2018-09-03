from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('api', views.api, name='api'),
	path('test', views.test, name='test'),
]
