from django.conf.urls import patterns, url
from links import views

urlpatterns = patterns('links.views',
    url(r'^link/settings/$', views.settings, name = 'settings'),
    url(r'^link/donate/(?P<url>[\d\w.]+)$', views.kintera_redirect, name = 'donate'),
    url(r'^link/rider/(?P<url>[\d\w.]+)$', views.t4k_redirect, name = 'profile'),
)