from django.core.urlresolvers import reverse
from django.http import *
from django.utils import simplejson as json

from contrib.replies.views import get_replies
from ublogging import uapi
from ublogging.models import Post, Image

from httpauth import http_auth
from django.http import *
from jsonize import *
from django.views.decorators import http
from django.core import serializers
from functools import partial

class JSONResponse(HttpResponse):
    def __init__(self, content, mimetype = "application/json",*args,**kwargs):
        #content = json.dumps(content)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
        
def curry(fn, *cargs, **ckwargs):
    def call_fn(*fargs, **fkwargs):
        d = ckwargs.copy()
        d.update(fkwargs)
        return fn(*(cargs + fargs), **d)
    return call_fn
    
jsonserializer = serializers.get_serializer('sjson')()
jsonize = partial(jsonserializer.serialize, ensure_ascii = False)

def user_timeline(request, username):
    posts = uapi.user_timeline(username, paginated=False)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


@http_auth
def auth_user_timeline(request):
    return user_timeline(request, request.user.username)


@http_auth
def replies(request):
    posts = get_replies(request)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def friends_timeline(request, username):
    posts = uapi.friends_timeline(username)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


@http_auth
def auth_friends_timeline(request):
    return friends_timeline(request, request.user.username)


def public_timeline(request):
    posts = uapi.public_timeline(paginated=False)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def show(request, id):
    post = jsonize_post(Post.objects.get(id=id))
    return HttpResponse(json.dumps(post),
            mimetype='application/json')


@http_auth
def update(request):
    user = request.user
    status = request.POST['status']
    post = uapi.new_post(user, status)
    return HttpResponse(json.dumps(jsonize_post(post)),
            mimetype='application/json')


@http_auth
def destroy(request, id):
    user = request.user

    p = Post.objects.filter(id=id)
    if p and p[0].user == user:
        p[0].delete()
        response = jsonize_post(p[0])
    else:
        rq = reverse(destroy, kwargs={'id':id})
        response = dict(request=rq, error="That's not yours.")

    return HttpResponse(json.dumps(response), mimetype='application/json')

@http_auth
def upload_image(request):
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        files = request.FILES.values()
        urls = []
        for file in files:
            image = Image(data = file)
            image.save()
            urls.append (image.data.url)
            #except:
            #   return HttpResponseServerError()
        return HttpResponse(json.dumps(urls), mimetype='application/json')
    else:
        #return HttpResponseRedirect('/')
        return HttpResponseBadRequest()

def place_list(request):
    places = Place.objects.all()
    #dumps = [jsonize(i, relations = ('owner')) for i in places]
    dumps = jsonize(places )#relations = ('owner'))
    return HttpResponse(dumps, mimetype='application/json')

def place_show(request, id):
    place = Place.objects.get(id = id)
    pObj = jsonize(place)
    return HttpResponse(pObj, mimetype='application/json')

def place_query(request):
    code = request.GET.get('code')
    if code is None:
        return HttpResponseBadRequest()
    else:
        place = Place.objects.filter(code=code)
        if place is None:
            return HttpResponseNotFound()
        else:
            return HttpResponse(jsonize(place), mimetype='application/json')

def place_comments(request, id):
    comments = PlaceComment.objects.filter(place = id)
    return HttpResponse(json.dumps(comments), mimetype = 'application/json')

def jsonResponse(obj):
    return HttpResponse(json.dumps(obj), mimetype = 'application/json')

def place_checkins(request, id):
    checkins = CheckIn.objects.filter(place = id)
    checkins = [jsonize_checkin(checkin) for checkin in checkins]
    #TODO
    return jsonResponse(checkins)

def place_followers(request, id):
    pfs = PlaceFollower.objects.filter(place= id)
    followers = [jsonize_profile(pf.follower) for pf in pfs]
    #dumps = jsonserializer.serialize(followers, ensure_ascii = False)
    return jsonResponse(followers)

@http_auth
def comment_place (request):
    if request.method == 'POST':
        postDict = request.POST;
        place = postDict['id']
        profile = Profile.objects.get(user = request.user)
        content = postDict['content']
        reply = postDict['reply']
        if reply:
            comment = PlaceComment(place = place, user = profile, content = content, reply = reply)
        else:
            comment = PlaceComment(place = place, user = profile, content = content)
        comment.save()
        return jsonResponse(comment)
    else:
        return HttpResponseBadRequest()

@http_auth
def checkin_place(request):
    if request.method == 'POST':
        place = request.POST.get('place', None)
        if not place:
            return HttpResponseBadRequest()
        place = Place.objects.get(id=int(place))
        if not place:
            return HttpResponseNotFound()
        comment = request.POST.get('comment', None)
        visible = request.POST.get('visible', 0)
        user = Profile.objects.get(user=request.user)
        
        pic = request.FILES.get('picture', None)
        picture = None
        if pic:
            picture = Image(data = pic)
        checkin = CheckIn(user = user, place = place, comment = comment, picture = picture, visible = int(visible))
        checkin.save()
        return JSONResponse(json.dumps(checkin, ensure_ascii=False))#relations=('user', 'place', 'picture')))
    else:
        return HttpResponseBadRequest()

@http_auth
@http.require_http_methods(['GET', 'POST'])
def follow_place(request):
    place = request.REQUEST.get('place', None)
    if not place:
        return HttpResponseBadRequest()
    place = Place.objects.get(id=int(place))
    if not place:
        return HttpResponseNotFound()
    user = Profile.objects.get(user=request.user)
    status = PlaceFollower.objects.filter(place=place, follower = user)
    if request.method == 'POST':
        if not status:
            pf = PlaceFollower(place = place, follower = user)
            pf.save()
        else:
            status.delete()
        return HttpResponse(status=200)
    else:
        if status:
            return HttpResponse('1')
        else:
            return HttpResponse('0')

@http_auth
#@http.require_http_methods(["GET", "POST"])
@http.require_GET
def user(request, id):
    user = Profile.objects.get(user = id)
    if user:
        return jsonResponse(jsonize_profile(user))
    else:
        return HttpResponseNotFound()

@http_auth
@http.require_http_methods(["GET", "POST"])
def mine(request):
    def edit(request, obj, fields):
        for field in fields:
            if field in request.POST and field in obj.__dict__:
                obj.__dict__[field] = request.POST[field]
        return obj 
    
    if request.method == "GET":
        profile = Profile.objects.get(user = request.user)
        if profile:
            return jsonResponse(jsonize_profile(profile))
        else:
            return HttpResponseNotFound()
    elif request.method == "POST":
        profile, created = Profile.objects.get_or_create(user = request.user)
        if profile:
            p = profile
        else:
            p = created
        fields = ['display', 'location', 'gender', 'age', 'addr', 'email', 'homepage', 'blog']
        p = edit (request, p, fields)
        p.save()
        return jsonResponse(p)

def user_followers(request, id):
    user = User.objects.get(id=id)
    if not user:
        return HttpResponseNotFound()
    followers = Follower.objects.filter(user=user)
    dicts = [jsonize_user(i) for i in followers]
    return jsonResponse(dicts)


@http_auth
@http.require_POST
def mail2user (request):
    pass

@http_auth
@http.require_http_methods(['GET', 'POST'])
def follow_user (request):
    #import pdb; pdb.set_trace()
    user = request.REQUEST.get('user', None)
    if not user:
        return HttpResponseBadRequest()
    user = User.objects.get(id = int(user))
    if user is None:
        return HttpResponseNotFound('User not found')
    cur = Follower.objects.filter(user=user, follower = request.user)
    if request.method == 'GET':
        if cur:
            resp = '1'
        else:
            resp = '0'
        return HttpResponse(resp)
    else:
        
        if not cur:
            uf = Follower (user = user, follower = request.user)
            uf.save()
        else:
            cur.delete()
        return HttpResponse(status = 200)

@http_auth
@http.require_POST
def comment_post(request):
    pass
