from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url(r'api/$', views.collection, name='collection'),
    url(r'api/embed_collection/$', views.embed_collection,
        name='embed_collection'),
    url(r'api/(\d+)/$', views.video, name='video'),
    url(r'api/(\d+)/embed/$', views.embed, name='embed'),
)
