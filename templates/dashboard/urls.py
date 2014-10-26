from django.conf.urls import patterns, url
from links import views

urlpatterns = patterns('links.views',
    url(r'^link/settings/$', views.settings, name = 'settings'),
    url(r'^link/stats/$', views.stats, name = 'stats'),
)
