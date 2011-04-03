from django.db.models import Q
from django.template.loader import render_to_string

from contrib.followers.models import Follower
from ublogging.api import Plugin


class FollowingList(Plugin):
    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not viewing_user and user and not user.is_authenticated():
            return ''
        else:
            user = viewing_user or user
            try:
                f_list = Follower.objects.filter(follower=user)
            except:
                return ''
            return render_to_string('following.html', { 'following': f_list })

    def headbar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        auth = user and user.is_authenticated()
        if not viewing_user or not auth:
            return ''

        if viewing_user == user:
            return ''

        user = viewing_user
        try:
            f = Follower.objects.get(user=user, follower= context.get('user', None))
            following = True
            image = u'followno'
        except:
            following = False
            image = u'follow'
        return render_to_string('follow.html',
                    {'user': user, 'image':image,
                     'MEDIA_URL': context['MEDIA_URL'],
                     'following': following})


class FollowerList(Plugin):
    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not viewing_user and user and not user.is_authenticated():
            return ''
        else:
            user = viewing_user or user

            try:
                f_list = Follower.objects.filter(user=user)
            except:
                return ''
            return render_to_string('follower.html', { 'followers': f_list })

    def post_list(self, value, request, user_name):
        return value | Q(user__in = Follower.objects.filter(follower=request.user).values('user'))
