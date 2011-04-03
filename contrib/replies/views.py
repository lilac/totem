import re

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from ublogging.views import paginate_list, refresh_index
from ublogging.models import Post


def get_replies(request, user_name=None):
    if user_name is None:
        user_name = request.user.username
    q = Q(text__contains = "@"+user_name)
    latest_post_list = Post.active().filter(q).order_by('-pub_date')

    return latest_post_list


def replies(request, user_name=None):
    latest_post_list = get_replies(request, user_name)
    latest_post_list = paginate_list(request, latest_post_list)
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list,
            'refresh_uri': '/replies/refresh',
        }, context_instance=RequestContext(request))


def refresh(request, lastid):
    url = request.META['HTTP_REFERER']
    usere = r'(.*)/replies/(?P<username>[^\?\/]*)'

    user_replies = re.match(usere, url)
    if user_replies:
        latest_post_list = get_replies(request, user_replies.group('username'))
    else:
        latest_post_list = get_replies(request)
    return refresh_index(request, lastid=lastid, latest_post_list=latest_post_list)


def replies_username(request, user_name):
    return replies(request, user_name)
