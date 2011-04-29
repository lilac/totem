'''
Created on Apr 29, 2011

@author: ivy
'''
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended

from ublogging.models import *

#profile_fields = Profile._meta.local
profile_fields = ('id', 'name', 'url', 'gender', 'location', 'province')
class AnonymousPlaceHandler(AnonymousBaseHandler):
    """
    Anonymous entrypoint for blogposts.
    """
    model = Place
    fields = ('id', 'name', 'addr', 'time', 'description', 'code',
              'homepage', 'rank', 'longitude', 'latitude',
              ('owner', profile_fields))
    exclude = ()
#    @classmethod
#    def resource_uri(self):
#        return ('blogposts', [ 'title', ])

class PlaceHandler(BaseHandler):
    """
    Authenticated entrypoint for places.
    """
    model = Place
    anonymous = AnonymousPlaceHandler
    
    fields = ('id', 'name', 'addr', 'time', 'description', 'code',
              'homepage', 'rank', 'longitude', 'latitude',
              ('owner', profile_fields))
    exclude = ()
    
    def read(self, request, id = None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.
        
        Parameters:
         - `title`: The title of the post to retrieve.
        """
        base = Place.objects
        #import pdb; pdb.set_trace()
        #id = request.GET
        if id:
            return base.get(id=id)
        else:
            return base.all()
    
#    def content_length(self, blogpost):
#        return len(blogpost.content)
        
#    @require_extended
#    def create(self, request):
#        """
#        Creates a new blogpost.
#        """
#        attrs = self.flatten_dict(request.POST)
#
#        if self.exists(**attrs):
#            return rc.DUPLICATE_ENTRY
#        else:
#            post = Place (title=attrs['title'], 
#                            content=attrs['content'],
#                            author=request.user)
#            post.save()
#            
#            return post
#    
#    @classmethod
#    def resource_uri(self):
#        return ('blogposts', [ 'title', ])

class PlaceQueryHandler (BaseHandler):
    
    def read(self, request):
        base = Place.objects
        code = request.GET.get('code')
        if code is None:
            resp = rc.BAD_REQUEST
            return resp
        else:
            return base.get(code=code)

class AnonymousCheckinHandler(BaseHandler):
    model = CheckIn
    allowed_methods = ('GET')
    def read(self, request, id = None):
        base = CheckIn.objects
        if not id:
            return base.all()
        else:
            return base.get(id=id)
       
class CheckinHandler (BaseHandler):
    model = CheckIn
    anonymous = AnonymousCheckinHandler
    def has_model(self):
        return True
    
    def read(self, request, id = None):
        base = CheckIn.objects
        if not id:
            return base.all()
        else:
            return base.get(id=id)
        
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        place = request.POST.get('place', None)
        if not place:
            return rc.BAD_REQUEST
        place = Place.objects.get(id=int(place))
        if not place:
            return rc.NOT_FOUND
        if self.exists(**attrs):
            return rc.DUPLICATE_ENTRY
        else:
            comment = request.POST.get('comment', None)
            visible = request.POST.get('visible', 0)
            #import pdb; pdb.set_trace()
            user = Profile.objects.get(user=request.user)
            
            pic = request.FILES.get('picture', None)
            picture = None
            if pic:
                picture = Image(data = pic)
                picture.save()
            checkin = CheckIn(user = user, place = place, comment = comment, picture = picture, visible = int(visible))
            checkin.save()
            return checkin


class CheckinUserTimelineHandler(BaseHandler):
    def read(self, request, username = None, id = None):
        base = CheckIn.objects
        if not id and not username:
            return base.all()
        elif id:
            user = User.get(id=id)
        else:
            user = User.objects.get(username=username)
            if not user:
                resp = rc.NOT_FOUND
                return resp
        checkins = base.filter(user=user)
        return checkins

class CheckinFriendTimelineHandler(BaseHandler):
    def read(self):
        base = CheckIn.objects
        
                

