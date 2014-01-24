from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('dashboard.views',
    url(r'^$', views.dashboard, name = 'dashboard'),
    url(r'^login/$', views.enter_gate, name = 'login'),
    url(r'^logout/$', views.exit_gate, name = 'logout'),
    url(r'^log/ride/$', views.log_ride, name = 'log_ride'),
)