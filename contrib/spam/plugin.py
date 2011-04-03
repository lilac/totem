import re

from django.template.loader import render_to_string
from ublogging.api import Plugin


class Spam(Plugin):

    __plugin_name__ = 'spam'

    def sidebar(self, context):

        return ''

    def tools(self, context, post):

        user = context.get('user', None)
        if not user or not user.is_superuser:
            return ''
        else:
            return render_to_string('spamtool.html',
                    {'post': post,
                     'MEDIA_URL': context['MEDIA_URL']})


    def posting(self, request, post):
        # TODO guess if it's an spam message
        return False
