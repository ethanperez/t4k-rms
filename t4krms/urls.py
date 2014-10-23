from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('dashboard.urls', namespace = "dashboard")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fitness/', include('fitness.urls', namespace = "fitness")),
)
