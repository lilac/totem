import re

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ublogging.uapi import Request_moc
from ublogging.uapi import paginate_list
from contrib.privatetimeline.models import PrivateSweet
from ublogging.models import Post
import ublogging


@login_required
def private_message(request):
    if request.POST.get('ajax', ''):
        receiver = request.POST.get('receiver', '')
        msg = request.POST.get('msg', '')
        receiver = get_object_or_404(User, username=receiver)
        privatesweet = PrivateSweet(sender=request.user, receiver=receiver, msg=msg)
        privatesweet.save()

        data = dict()
        return HttpResponse(json.dumps(data), mimetype='application/json')

    url = request.META.get('HTTP_REFERER', reverse('ublogging.views.index'))
    return HttpResponseRedirect(url)

@login_required
def private_reply(request):
    if request.POST.get('ajax', ''):
        sweet_id = request.POST.get('sweet_id', '')
        receiver = request.POST.get('receiver', '')
        msg = request.POST.get('msg', '')
        sweet = get_object_or_404(Post, id=sweet_id)
        receiver = get_object_or_404(User, username=receiver)
        privatesweet = PrivateSweet(sender=request.user, receiver=receiver, msg=msg)
        privatesweet.save()
        data = dict()
        return HttpResponse(json.dumps(data), mimetype='application/json')

    url = request.META.get('HTTP_REFERER', reverse('ublogging.views.index'))
    return HttpResponseRedirect(url)


def get_private_timeline(request, paginated=True):
    if (request.user.is_authenticated()):
        latest_privs_list = PrivateSweet.objects.filter(receiver=request.user).order_by('-msg_date')
        if paginated:
            latest_privs_list = paginate_list(request, latest_privs_list)
        return latest_privs_list
    else:
        raise Exception("Not authenticated")

@login_required
def private_timeline(request):
    latest_privs_list = get_private_timeline(request)

    return render_to_response('privatetimeline.html', {
            'latest_privs_list': latest_privs_list,
            'page': request.GET.get('page', '1')
        }, context_instance=RequestContext(request))


@login_required
def private_remove(request, privid):
    priv = get_object_or_404(PrivateSweet, id=privid)
    if priv.receiver != request.user:
        return HttpResponseRedirect(reverse(private_timeline))
    else:
        priv.delete()
        return HttpResponseRedirect(reverse(private_timeline))
