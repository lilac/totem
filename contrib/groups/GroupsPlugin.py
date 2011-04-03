from django.template.loader import render_to_string

from contrib.groups.models import Group
from ublogging.api import Plugin


class GroupHooks(Plugin):
    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not user:
            return ''
        if not viewing_user and not user.is_authenticated():
            return ''
        else:
            user = viewing_user or user
            return render_to_string('groupsidebar.html', {
                    'group_list': Group.objects.filter(users__user=user),
                })
