from django.conf.urls import patterns, url
from adminlinks import views

urlpatterns = patterns('adminlinks.views',
    url(r'^(?P<dalink>[\d\w.]+)$', views.goto, name = 'goto'),
)