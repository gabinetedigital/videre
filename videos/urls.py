from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url(r'api/(\d+)/$', views.video, name='video'),
)
