from django.conf.urls.defaults import *

urlpatterns = patterns('ublogging.views',
    (r'^$', 'index'),
    (r'sweet/(?P<sweetid>\d+)$', 'sweet'),
    (r'public_timeline', 'public_timeline'),
    (r'status/new', 'new'),
    (r'user/(?P<user_name>.*)$','user'),
    (r'refresh/(?P<lastid>\d+)$', 'refresh_index'),
    (r'refresh$', 'refresh_index'),
    (r'validate/(\w+)$', 'validate'),
    (r'profile','profile'),
    (r'renewapikey','renewapikey'),
)
