import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from django.utils.translation import ugettext as _

from contrib.karma.models import Vote, KarmaSweet
from ublogging.models import Post


@login_required
def vote(request, sweet_id):
    real_vote(request, sweet_id)
    sweet = get_object_or_404(Post, id=sweet_id)
    if request.POST.get('ajax', ''):
        karma = get_object_or_404(KarmaSweet, sweet=sweet)
        positives = Vote.objects.filter(sweet=sweet, vote=1).count()
        negatives = Vote.objects.filter(sweet=sweet, vote=-1).count()
        data = dict(karma=karma.karma, positives=positives,
                negatives=negatives)
        return HttpResponse(json.dumps(data),
                            mimetype='application/json')
    url = request.META.get('HTTP_REFERER',
                           reverse('ublogging.views.index'))
    return HttpResponseRedirect(url)


@login_required
def real_vote(request, sweet_id):
    if request.method == 'GET':
        return False

    sweet = get_object_or_404(Post, id=sweet_id)
    if request.user == sweet.user:
        return False

    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    if sweet.pub_date < yesterday:
        return False

    sum = int(request.POST.get('vote', 1))
    # a vote must be positive or negative
    if not (sum == -1 or sum == 1):
        return False
    try:
        new_vote = Vote(user=request.user, sweet=sweet, vote=sum)
        new_vote.save()
    except:
        return False

    return True
