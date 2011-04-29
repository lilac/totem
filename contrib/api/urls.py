from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from contrib.api.handlers import *

auth = HttpBasicAuthentication(realm='Totem API')

places = Resource(PlaceHandler)
place_query = Resource(PlaceQueryHandler)

checkins = Resource(CheckinHandler, authentication=auth)

checkins_user_timeline = Resource(CheckinUserTimelineHandler, authentication=auth)

urlpatterns = patterns('', 
    # piston api
    url(r'places/$', places),
    url(r'places\.(?P<emitter_format>\w+)', places),
    url(r'places/(?P<id>\d+).(?P<emitter_format>[a-z]+)/$', places),#FIXME
    url(r'places/query.(?P<emitter_format>\w+)', place_query),  
    
    #checkins
    (r'checkins/(?P<id>\d+).(?P<emitter_format>[a-z]+)/$', checkins),
    (r'checkins\.json$', checkins),
    (r'checkins/user_timeline/(?P<username>\w+)\.(?P<emitter_format>[a-z]+)/$',
     checkins_user_timeline),
    
    (r'checkins/public_timeline\.(?P<emitter_format>[a-z]+)/$', checkins),
                         

)
urlpatterns += patterns('contrib.api.views',
    (r'statuses/user_timeline/(?P<username>\w+).json', 'user_timeline'),
    (r'statuses/user_timeline.json', 'auth_user_timeline'),
    (r'statuses/replies.json', 'replies'),
    (r'statuses/friends_timeline/(?P<username>\w+).json', 'friends_timeline'),
    (r'statuses/friends_timeline.json', 'auth_friends_timeline'),
    (r'statuses/public_timeline.json', 'public_timeline'),
    (r'statuses/show/(?P<id>\d+).json', 'show'),
    (r'statuses/update.json', 'update'),
    (r'statuses/destroy/(?P<id>\d+).json', 'destroy'),
	(r'image/upload.json', 'upload_image'),
    
    
	# show place info
    #(r'places.json', 'place_list'),
	(r'places/(?P<id>\d+).json', 'place_show'),
	(r'places/(?P<id>\d+)/comments.json', 'place_comments'),
	(r'places/(?P<id>\d+)/checkins.json', 'place_checkins'),
	(r'places/(?P<id>\d+)/followers.json', 'place_followers'),
    #(r'places/query.json', 'place_query'),
	# place operation
	(r'places/comment.json', 'comment_place'),
	(r'places/checkin.json', 'checkin_place'),
	(r'places/follow.json', 'follow_place'),
	# show user info
	(r'users/(?P<id>\d+).json', 'user'),
	(r'users/mine.json', 'mine'), # get or post
	(r'users/(?P<id>\d+)/followers.json', 'user_followers'),
	# user operation
	(r'users/follow.json', 'follow_user'),
    #(r'users/edit.json', 'edit_user'),
	(r'users/mail.json', 'mail2user'),
    # show post
    (r'posts/(?P<id>\d+).json', 'show'),
	# post operation
	(r'posts/comment.json', 'comment_post'),
)
