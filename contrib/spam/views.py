from ublogging.models import Post
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def mark(request, pid):
    post = get_object_or_404(Post, pk=pid)
    user = post.user
    user.delete()

    url = request.META.get("HTTP_REFERER", reverse('ublogging.views.public_timeline'))
    return HttpResponseRedirect(url)
