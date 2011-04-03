from django.core.management.base import BaseCommand, CommandError
import datetime

DATE = datetime.datetime.now() - datetime.timedelta(1)

RATIO1 = 0.80
RATIO2 = 0.60

class Command(BaseCommand):
    args = ''
    help = 'Down the users and sweets karma'

    def handle(self, *args, **options):
        self.down_user_karma()
        self.down_sweet_karma()


    def down_user_karma(self):
        from contrib.karma.models import Karma
        from ublogging.models import Post
        all = Karma.objects.exclude(karma=0.0)
        for karma in all:
            n = Post.active().filter(user=karma.user,
                            pub_date__gt=DATE).count()

            ratio = RATIO2
            if n:
                ratio = RATIO1

            karma.karma = karma.karma * ratio
            karma.save()


    def down_sweet_karma(self):
        from contrib.karma.models import KarmaSweet
        all = KarmaSweet.objects.exclude(karma=0.0)
        for karmasweet in all:
            karmasweet.karma = karmasweet.karma * RATIO1
            karmasweet.save()
