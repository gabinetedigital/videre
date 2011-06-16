from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('videos.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # static media
    url(r'^s/(.*)', 'django.views.static.serve',
        {'document_root': 'static'},
        name='static'),
)
