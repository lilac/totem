from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

from ublogging.feeds import PublicTimeline, UserTimeline

feeds = {
    'public': PublicTimeline,
    'user': UserTimeline,
}

urlpatterns = patterns('',
    (r'^sweetter/', include('ublogging.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'login.html'}),
    (r'^logout/$', 'ublogging.views.logout'),
    (r'^join/$', 'ublogging.views.join'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
                        {'feed_dict': feeds}),
    (r'^$', 'ublogging.views.index'),
	#(r'image/upload', 'ublogging.views.upload_image'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    (r'^recover/', include('contrib.recoverpw.urls')),
    (r'^groups/', include('contrib.groups.urls')),
    (r'^replies/', include('contrib.replies.urls')),
    (r'^privatetimeline/', include('contrib.privatetimeline.urls')),
    (r'^spam/', include('contrib.spam.urls')),
    (r'^remove/', include('contrib.remove.urls')),
    (r'^sweetter/karma/', include('contrib.karma.urls')),
    (r'^sweetter/follow/(?P<user_id>\d+)/$', 'contrib.followers.views.follow'),
    (r'^api/', include('contrib.api.urls')),
   )
