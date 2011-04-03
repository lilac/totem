from django.conf import settings
from django.core.urlresolvers import reverse

from ublogging.api import Plugin


class RemovePlugin(Plugin):

    def tools(self, context, post):
        user = context.get('user', None)
        if not user:
            return ''
        if not user.is_authenticated() or \
               (post.user.username != user.username):
            return ''

        url = reverse('contrib.remove.views.remove', args=[post.id])

        link = '''<div
            style="background: transparent url('%sremove.png') no-repeat; padding-left: 16px;">
            <a href="%s">delete</a></div>'''

        return link % (settings.MEDIA_URL, url)
