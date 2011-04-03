import textparsers
import urllib
import hashlib

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

import ublogging


register = template.Library()


@register.filter
@stringfilter
def parse(value):
    for p in ublogging.plugins + textparsers.parsers:
        value = p.parse(value)
    return value

@register.inclusion_tag("privatesweet.html", takes_context='True')
def format_private_sweet(context, sweet):
    return {'post': sweet, 'context':context, 'MEDIA_URL': settings.MEDIA_URL}

