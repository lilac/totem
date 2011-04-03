from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings

from ublogging.models import Post

class PrivateSweet(models.Model):
    receiver = models.ForeignKey(User, related_name='receivers')
    sender = models.ForeignKey(User, related_name='senders')
    msg = models.TextField()
    msg_date = models.DateTimeField(auto_now=True)

    def sender_key(self):
        from PrivateTimelinePlugin import PrivateTimelinePlugin
        p = PrivateTimelinePlugin()
        return p.gpg_key_id.get_value(self.sender.username)


def notify_sweet(sender, **kwargs):
    p = kwargs['instance']
    subject = _('%s sends you a private message') % p.sender.username
    msg = _('''
%s sends you a private message:
---
%s
---
You can view your private messages in:
%s
    ''') % (p.sender.username, p.msg, settings.DOMAIN + reverse('contrib.privatetimeline.views.private_timeline'))
    send_mail(subject, msg, settings.MSG_FROM,
                [p.receiver.email], fail_silently=False)


post_save.connect(notify_sweet, sender=PrivateSweet)
