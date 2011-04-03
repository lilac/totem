from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from ublogging.api import Plugin
#from django.template import RequestContext
from django.core.context_processors import csrf


class UserForm(Plugin):
    def sidebar(self, context):
        user = context.get('user', None)
        viewing_user = context.get('viewing_user', None)
        if not user:
            return ''
        if not viewing_user and user and not user.is_authenticated():
            form = AuthenticationForm(context['request'].POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                user_authenticated = authenticate(username=form.cleaned_data.username, password=form.cleaned_data.password)
                if user_authenticated is not None and user_authenticated.is_active:
                    # user logged in succesfully
                    user_authenticated.login(context['request'], user_authenticated)
                    context['user'] = user_authenticated
                    return u'Thanks'
                else:
                    form = AuthenticationForm()
            else:
                form = AuthenticationForm()
            #context = RequestContext (context['request'])
            c = {'form': form}
            c.update (csrf(context['request']))
            return render_to_string('loginform.html', c)
        else:
            return render_to_string('loggedin.html', context_instance=context)
