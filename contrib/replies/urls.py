from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.replies.views',
    (r'refresh/(?P<lastid>\d+)$', 'refresh'),
    (r'^$', 'replies'),
    (r'^(?P<user_name>.*)/$', 'replies_username'),
)
