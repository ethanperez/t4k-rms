from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('dashboard.views',
    url(r'^$', views.dashboard, name = 'dashboard'),
    url(r'^team/stats/$', views.all_riders, name = 'team_stats'),
    url(r'^riders/(?P<rider>\d+)$', views.dashboard, name = 'dashboard'),
    url(r'^login/$', views.enter_gate, name = 'login'),
    url(r'^logout/$', views.exit_gate, name = 'logout'),
    url(r'^log/ride/$', views.log_ride, name = 'log_ride'),
    url(r'^profile/change_password/$', views.change_password, name = 'change_password'),
    url(r'^first_login/$', views.first_login, name = 'first_login'),
)
