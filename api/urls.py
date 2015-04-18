from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('api.views',
    url(r'^account/$', views.account, name = 'account'),
    url(r'^rides/$', views.rides, name = 'rides')
)