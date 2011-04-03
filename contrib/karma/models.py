from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save

from ublogging.models import Post


NEGATIVE_VOTE = -0.05
VOTE_SCALE = 0.05


class Karma(models.Model):
    user = models.ForeignKey(User, unique=True)
    karma = models.FloatField(default=0)

    def __unicode__(self):
        return "%s - %f" % (self.user.username, self.karma)


class KarmaSweet(models.Model):
    sweet = models.ForeignKey(Post)
    karma = models.FloatField(default=0)

    def positives(self):
        return Vote.objects.filter(sweet=self.sweet, vote=1).count()

    def negatives(self):
        return Vote.objects.filter(sweet=self.sweet, vote=-1).count()

    def __unicode__(self):
        return "%s - %s - %f" % (self.sweet.user.username,
                                 self.sweet.text,
                                 self.karma)


class Vote(models.Model):

    class Meta:
        unique_together = ("user", "sweet")

    user = models.ForeignKey(User)
    sweet = models.ForeignKey(Post)
    vote = models.SmallIntegerField()
    vote_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s - %s - %d" % (self.user.username,
                                      self.sweet.user.username,
                                      self.sweet.text,
                                      self.vote)


class Log(models.Model):
    user = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now=True)
    karma = models.FloatField()

    def __unicode__(self):
        return "%s - %f" % (self.user.username,
                            self.karma)


def karma_updated(sender, **kwargs):
    karma = kwargs['instance']
    if karma.karma > 25:
        karma.karma = 25
    elif karma.karma < -10:
        karma.karma = -10
    log = Log(user=karma.user, karma=karma.karma)
    log.save()


def sweet_voted(sender, **kwargs):
    vote = kwargs['instance']
    try:
        voter_karma = Karma.objects.get(user=vote.user)
    except:
        voter_karma = Karma(user=vote.user)
        voter_karma.save()
    voter_karma = voter_karma.karma
    # if voter karma is negative is like no karma
    if voter_karma < 0:
        voter_karma = 0

    vote_n = vote.vote
    # positive votes depends on voter karma
    if vote_n > 0:
        vote_n = vote_n * VOTE_SCALE * voter_karma
        # a positive vote count at less as VOTE_SCALE
        if vote_n < VOTE_SCALE:
            vote_n = VOTE_SCALE
    # negative votes are constant
    else:
        vote_n = NEGATIVE_VOTE

    try:
        voted_karma = Karma.objects.get(user=vote.sweet.user)
    except:
        voted_karma = Karma(user=vote.sweet.user)

    new_karma = voted_karma.karma + vote_n
    voted_karma.karma = new_karma
    voted_karma.save()

    try:
        sweet_karma = KarmaSweet.objects.get(sweet=vote.sweet)
    except:
        sweet_karma = KarmaSweet(sweet=vote.sweet)

    new_sweet_karma = sweet_karma.karma + vote_n
    sweet_karma.karma = new_sweet_karma
    sweet_karma.save()


def new_post(sender, **kwargs):
    post = kwargs['instance']
    try:
        karma = Karma.objects.get(user=post.user)
    except:
        karma = Karma(user=post.user)
    karma.karma += VOTE_SCALE
    karma.save()


def penalize(sender, **kwargs):
    post = kwargs['instance']
    try:
        karma = Karma.objects.get(user=post.user)
    except:
        karma = Karma(user=post.user)
    karma.karma -= VOTE_SCALE
    karma.save()


def delete_log(sender, **kwargs):
    user = kwargs['instance']
    logs = Log.objects.filter(user=user)
    logs.delete()


# To log all changes in karma
pre_save.connect(karma_updated, sender=Karma)
# To change the karma when someone vote
post_save.connect(sweet_voted, sender=Vote)
# Every post increase the karma
post_save.connect(new_post, sender=Post)
pre_delete.connect(penalize, sender=Post)
pre_delete.connect(delete_log, sender=User)
