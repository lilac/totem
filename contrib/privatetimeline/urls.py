from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.privatetimeline.views',
    (r'^$', 'private_timeline'),
    (r'^new$', 'private_message'),
    (r'^reply$', 'private_reply'),
    (r'^remove/(\d+)$', 'private_remove')
)
