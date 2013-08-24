from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('baidumusic.views',
    url(r'^$', 'home', name='home'),
    url(r'^song/(?P<song_id>\d+)$', 'song', name='song'),
)
