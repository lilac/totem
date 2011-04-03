import datetime

from django.template.loader import render_to_string

from ublogging.api import Plugin
from contrib.karma.models import Karma, KarmaSweet, Vote


class KarmaCount(Plugin):

    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if viewing_user:
            user = viewing_user
        else:
            if user and not user.is_authenticated():
                user = None

        if user:
            try:
                k = Karma.objects.get(user=user)
            except:
                k = Karma(user=user)
                k.save()
        else:
            k = False
        karma_ranking = Karma.objects.all().order_by('-karma')[:5]
        sweet_karma_ranking = KarmaSweet.objects.all().order_by('-karma')[:5]

        return render_to_string('karmasidebar.html',
                                {'karma': k,
                                 'karma_ranking': karma_ranking,
                                 'sweet_karma_ranking': sweet_karma_ranking,
                                })

    def tools(self, context, post):
        user = context.get('user', None)
        if not user:
            return ''
        if not user.is_authenticated():
            return ''
        try:
            k = KarmaSweet.objects.get(sweet=post)
        except:
            k = KarmaSweet(sweet=post)
            k.save()

        voted = Vote.objects.filter(sweet=post, user=user).count()

        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        expired = False
        if post.pub_date < yesterday:
            expired = True

        return render_to_string('karmatool.html',
                                {'karma': k,
                                 'sweet': post,
                                 'auth_user': user,
                                 'expired': expired,
                                 'MEDIA_URL': context['MEDIA_URL'],
                                 'voted': voted})
