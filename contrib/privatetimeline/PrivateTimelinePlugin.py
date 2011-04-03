import re

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from ublogging.api import Plugin
from ublogging.models import Post
from ublogging.api import PluginOpt

from models import PrivateSweet


class PrivateTimelinePlugin(Plugin):
    '''
    With this plugin users can send a private and encrypted message to somebody, which will be
    shown only in the private timeline of that user. The message will be encrypted with GPG using
    a HTML extension currently only available in Khtml/Konqueror.

    Each user can access their private timeline with a link added by this plugin in the top list of
    links, and messages can be sent to a given user by clicking the "private reply" tool button of
    a sweet of that user, or clicking in the "Send private sweet" in the sidebar of the user.
    '''

    __plugin_name__ = 'private_timeline'
    gpg_key_id = PluginOpt('private_timeline__gpg_key_id')

    def headbar(self, context):
        '''
        Shows a button to 'Send Private Message to <username>' in the headbar,
        next to "(un)follow" button
        '''

        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not viewing_user or not user.is_authenticated():
            return ''

        keyid = self.gpg_key_id.get_value(viewing_user.username)

        send_private_link = ('<a href="" title="%s;%s" class="private_message">%s</a>') %\
                                            (viewing_user.username, keyid, _('Send Private Message'))
        return send_private_link


    def sidebar(self, context):
        '''
        Shows a link to 'Send Private Message' in the sidebar when browsing a profile
        '''

        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        ret = render_to_string('privatesweetform.html',
                {'MEDIA_URL': context.get('MEDIA_URL', '')})

        purl = reverse('contrib.privatetimeline.views.private_timeline')

        if user.is_authenticated():
            pn = PrivateSweet.objects.filter(receiver=user).count()
        else:
            pn = 0

        private_link = '<a href="%s">%s (%s)</a>' % (purl, _('Private Timeline'), pn)

        if not viewing_user:
            if user.is_authenticated():
                ret = '<div class="priv_sidebar">%s<br/>%s</div>' % (ret, private_link)
            return ret

        keyid = self.gpg_key_id.get_value(viewing_user.username)
        send_private_link = ('<a href="" title="%s;%s" class="private_message">%s</a>') %\
                                            (viewing_user.username, keyid, _('Send Private Message'))

        return '''<div class="priv_sidebar">%s<br/>%s<br/>%s</div>''' %\
                        (ret, private_link, send_private_link)


    def tools(self, context, post):
        '''
        Shows a tool to reply privately a message
        '''
        user = context.get('user', None)
        if not user or not user.is_authenticated():
            return ''

        if post.user == user:
            return ''

        keyid = self.gpg_key_id.get_value(post.user.username)

        return render_to_string('privatereply.html',
                {'reply_user': post.user,
                 'keyid': keyid,
                 'post' : post,
                 'MEDIA_URL': context['MEDIA_URL']})
