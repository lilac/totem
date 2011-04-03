from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from ublogging.api import Plugin


class Recover(Plugin):

    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not user:
            return ''
        if not viewing_user and not user.is_authenticated():
            pr = _("Password recovery")
            return '<a href="'+reverse('contrib.recoverpw.views.index')+'">'+pr+'</a>'
        else:
            return ""
