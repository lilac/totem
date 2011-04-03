from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.spam.views',
    (r'^mark/(\d+)$', 'mark'),
)
