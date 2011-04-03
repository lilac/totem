import re

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from ublogging.api import Plugin
from ublogging.models import Post


class RepliesPlugin(Plugin):

    def __init__(self):
        self.script = '''
<script>
    $(".reply").click(function(){
        username = $(this).attr("title");
        $("#text")[0].value += "@" + username;
        $("#text").focus();
        return false;
    });
</script>
'''

    def parse(self, value):
        regex = re.compile("[:punct:]*(@[A-Za-z_\-\d]*)[:punct:]*")
        matches = re.findall(regex, value)
        if matches:
            dict = { }
            for match in matches:
                url = reverse('ublogging.views.user', args=[match[1:]])
                text = '<a href="'+url+'">'+match+'</a>'
                dict[match] = text
            for key in dict:
                value = value.replace(key, dict[key])
        return value

    def post_list(self, value, request, user_name):
        return value | Q(text__contains = "@"+user_name)

    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not viewing_user and not user.is_authenticated():
            return ''
        else:
            user = viewing_user or user
            replies = str(Post.active().filter(text__contains="@"+user.username).count())
            posts = str(Post.active().filter(user=user).count())
            url = reverse('contrib.replies.views.replies')
            return self.script +\
                    '<a href="'+url+'">'+_('Replies')+'</a>: '+replies+\
                    ' | '+_('Sweets')+': '+posts

    def tools(self, context, post):
        user = context.get('user', None)
        if not user:
            return ''
        if user.is_authenticated() and (post.user.username == user.username):
            return ''

        return render_to_string('reply.html',
                {'reply_user': post.user,
                 'MEDIA_URL': context['MEDIA_URL']})
