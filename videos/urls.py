from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.collection, name='collection'),
    url(r'^embed_collection/$', views.embed_collection,
        name='embed_collection'),
    url(r'^(\d+)/$', views.video, name='video'),
    url(r'^(\d+)/embed/$', views.embed, name='embed'),
)
