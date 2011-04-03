import textparsers
import urllib
import hashlib

from django import template
from django.template.defaultfilters import stringfilter

import ublogging


register = template.Library()


@register.filter
@stringfilter
def parse(value):
    for p in ublogging.plugins + textparsers.parsers:
        value = p.parse(value)
    return value


@register.inclusion_tag("status/sweet.html", takes_context='True')
def format_sweet(context, sweet):
    return {'post': sweet, 'context':context}


@register.simple_tag
def gravatar(email, size=48):

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode(
            {'gravatar_id':hashlib.md5(email.lower()).hexdigest(),
              'size':str(size),
              'd': 'identicon'})
    return gravatar_url


@register.tag("sidebar")
def do_sidebar(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires no arguments" % token.contents.split()[0]
    return SidebarNode()


class SidebarNode(template.Node):

    def render(self, context):
        s = ''.join(p.sidebar(context) for p in ublogging.plugins)
        return s


@register.tag("headbar")
def do_headbar(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires no arguments" % token.contents.split()[0]
    return HeadbarNode()


class HeadbarNode(template.Node):

    def render(self, context):
        s1 = ''.join(p.headbar(context) for p in ublogging.plugins)
        if s1:
            s = '<div id="headbar">%s</div>' % s1
        else:
            s = ''
        return s


@register.tag("tools")
def do_tools(parser, token):
    try:
        tag_name, post = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return ToolsNode(post)

class ToolsNode(template.Node):

    def __init__(self, post):
        self.post = template.Variable(post)

    def render(self, context):
        post = self.post.resolve(context)
        new_context = context['context']
        s = ''.join(p.tools(new_context, post) for p in ublogging.plugins if p.tools)
        return s

@register.tag("links")
def do_links(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires no arguments" % token.contents.split()[0]
    return LinksNode()

class LinksNode(template.Node):

    def render(self, context):
        s = ''.join(p.links(context) for p in ublogging.plugins if p.links)
        return s
