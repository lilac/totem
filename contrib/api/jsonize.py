import datetime
import time
import urllib, hashlib

from ublogging.models import *
from contrib.followers.models import Follower


def jsonize_post(post):
    user = jsonize_user(post.user)
    created_at = post.pub_date + datetime.timedelta(seconds=time.timezone)
    created_at = created_at.strftime("%a, %d %b %Y %H:%M:%S")

    post_data = dict(user=user,
                    created_at=created_at,
                    id=post.id,
                    text=post.text,
                    source = post.source)

    return post_data


def jsonize_user(user):
    p = Profile.objects.get(user=user)
    #user_data = dict(url=p.url,
    #                location=p.location,
    #                screen_name=user.username,
    #                name=user.username,
    #                profile_image_url=gravatar(user.email))
    user_data = jsonize_profile(p)

    return user_data


def jsonize_profile(p):
    flc = Follower.objects.filter(user = p.user).count()
    frc = Follower.objects.filter(follower = p.user).count()
    sc = Post.objects.filter(user = p.user).count()
    created_at = p.time + datetime.timedelta(seconds=time.timezone)
    created_at = created_at.strftime("%a, %d %b %Y %H:%M:%S")
    def get_image_url(image):
        if image is None:
            return None
        else:
            return image.data
    
    profile_dict = dict(id = p.id,
                        url = p.url,
                        location = p.location,
                        screen_name = p.user.username,
                        name = p.name,
                        profile_image_url = gravatar(p.user.email),
                        gender = p.gender,
                        province = p.province,
                        city = p.city,
                        description = p.description,
                        blog = p.blog,
                        icon = get_image_url(p.icon),
                        created_at = created_at,
                        followers_count = flc,
                        friends_count = frc,
                        statuses_count = sc,
                        vip = p.vip,
                        bonus = p.bonus,
                        rank = p.rank)
    return profile_dict

def fields(o, fields):
    dict = {}
    for f in fields:
        dict[f] = getattr(o, f)
    return dict

def jsonize_place(place):
    owner = jsonize_user(place.owner)
    #dict = place.__dict__
    dict = fields(place, ('id', 'name', 'time'))
    dict['owner'] = owner
    return dict
    #===========================================================================
    # dict = dict(id = place.id,
    #            name = place.name)
    #===========================================================================
def jsonize_place_comment(comment):
    user = jsonize_user(comment.user)
    place = jsonize_place(comment.place)
    dict = comment.__dict__
    dict['user'] = user
    dict['place'] = place
    return dict

def gravatar(email, size=48):
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email.lower()).hexdigest(), 'size':str(size)})
    return gravatar_url
