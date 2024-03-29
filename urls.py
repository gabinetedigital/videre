from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('videos.urls')),
)

if 'debug_toolbar_htmltidy' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^', include('debug_toolbar_htmltidy.urls')),
    )

# Static files
urlpatterns += staticfiles_urlpatterns()
