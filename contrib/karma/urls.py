from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.karma.views',
    (r'^vote/(?P<sweet_id>\d+)/$', 'vote'),
)
