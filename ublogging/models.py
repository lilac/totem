import string
import random

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm, ValidationError
from time import gmtime, strftime

#from django.utils import formats
#
#date_format = formats.get_format('DATE_FORMAT')
#datetime_format = formats.get_format('DATETIME_FORMAT')
#time_format = formats.get_format('TIME_FORMAT')

def generate_apikey():
    chars = string.letters + string.digits
    return "".join([random.choice(chars) for i in range(20)])

class Image(models.Model):
    user = models.ForeignKey('Profile')
    time = models.DateTimeField('upload time', auto_now = True)
    data = models.ImageField(upload_to = strftime('images/%Y/%m/%d', gmtime()))
    def __unicode__ (self):
        return 'Image of ' + self.user.name + ' uploaded at ' + str(self.time)

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length = 20)# display name
    apikey = models.CharField(max_length=20)
    url = models.URLField(blank = True)
    location = models.CharField(max_length=200, blank = True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Unknown')
    )
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = 'N')
    #age = models.SmallIntegerField()
    province = models.CharField(max_length = 20, blank = True)
    city = models.CharField(max_length = 20, blank = True)
    email = models.EmailField(blank = True)
#    city = models.CharField (max_length = 50)
    time = models.DateTimeField ('join time', auto_now = True)
    description = models.TextField(blank = True)
    #homepage = models.URLField()
    blog = models.URLField(blank = True)
    icon = models.ForeignKey(Image, blank = True, null = True)
    # Meta info for site
    bonus = models.PositiveIntegerField(default = 0)
    rank = models.PositiveSmallIntegerField(default = 1)
    vip = models.BooleanField(default = False)

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.regen_apikey()
            #self.location = "sweetter city"
            self.url = reverse("ublogging.views.user", kwargs={'user_name':self.user.username})
        super(Profile, self).save(*args, **kwargs)

    def regen_apikey(self):
        self.apikey = generate_apikey()
        while Profile.objects.filter(apikey=self.apikey).count():
            self.apikey = generate_apikey()

class Option(models.Model):
    optid = models.CharField(max_length=20)
    data = models.TextField()
    #type could be:
    #   int, str, password, bool
    type = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    unique_together = ("optid", "user")

    def __unicode__(self):
        return '<%s, %s, %s>' % (self.user.username, self.optid, self.data)


class Post(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('date published', auto_now=True)

    # repost
    upstream = models.OneToOneField('self', blank = True, null = True)

    # Meta infos.
    source = models.CharField (max_length = 20, default = "Android")
    @classmethod
    def active(klass):
        return klass.objects.filter(user__is_active=True)

    def __unicode__(self):
        return self.text

def user_post_save(sender, instance, signal, *args, **kwargs):
    # Creates user profile
    profile, new = Profile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)

# RegisterProfile
class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError(u'Email addresses must be unique.')
        return email


class Place(models.Model):
    name = models.CharField(max_length = 100)
    addr = models.CharField(max_length = 200, blank = True)
    description = models.TextField(blank = True)
    time = models.DateTimeField('date added', auto_now = True)
    owner = models.ForeignKey(Profile)
    code = models.CharField(max_length = 16, unique = True)
    homepage = models.URLField(max_length = 200, blank = True)
    rank = models.IntegerField(default = 1)
    latitude = models.IntegerField(blank = True, null = True)
    longitude = models.IntegerField(blank = True, null = True)
    #followers = models.ManyToManyField(User)
    
    def __unicode__ (self):
        return self.name

class PlaceFollower(models.Model):
    place = models.ForeignKey(Place)
    follower = models.ForeignKey(Profile)
    def __unicode__ (self):
        return self.place.name + " followed by " + self.follower.name

class CheckIn(models.Model):
    user = models.ForeignKey(Profile)
    place = models.ForeignKey(Place)
    time = models.DateTimeField('Check in time', auto_now = True)
    comment = models.TextField(blank = True)
    picture = models.ForeignKey(Image, blank = True, null = True)
    visible = models.IntegerField(default = 0)

    class Meta:
        ordering = ['-time']
    
    def __unicode__(self):
        return self.place.name + " checked by " + self.user.name

class PostComment(models.Model):
    user = models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
    content = models.TextField()
    time = models.DateTimeField('submit time', auto_now = True)
    reply = models.ForeignKey('self', blank = True, null = True) #TODO: I am not sured.
    
    def __unicode__(self):
        return self.user.name + '\'s post comment ' + 'at ' + str(self.time)
class PlaceComment (models.Model):
    user = models.ForeignKey(Profile)
    place = models.ForeignKey(Place)
    content = models.TextField()
    time = models.DateTimeField('submit time', auto_now = True)
    reply = models.ForeignKey('self', blank = True, null = True)
    def __unicode__(self):
        return self.user.name + '\'s place comment ' + 'at ' + str(self.time)

class CheckInComment (models.Model):
    user = models.ForeignKey(Profile)
    checkin = models.ForeignKey(CheckIn)
    content = models.TextField()
    time = models.DateTimeField('submit time', auto_now = True)
    reply = models.ForeignKey('self', blank = True, null = True)
    def __unicode__(self):
        return self.user.name + '\'s checkin comment ' + 'at ' + str(self.time)

class Mail (models.Model):
    sender = models.ForeignKey(Profile, related_name = 'sender')
    receiver = models.ForeignKey(Profile, related_name = 'receiver')
    content = models.TextField()
    time = models.DateTimeField('send time', auto_now = True)
    read = models.BooleanField(default = False)
    def __unicode__ (self):
        return 'Mail sent by ' + self.sender.name + ' to ' + self.receiver.name
        + ' at ' + self.time 

class PhotoGallery(models.Model):
    user = models.ForeignKey(Profile)
    name = models.CharField(max_length = 200, default = "untitled")
    photo = models.ForeignKey(Image)
    def __unicode__(self):
        return "Photo gallery: " + self.name + ' of ' + self.user.name

class PlacePicture(models.Model):
    place = models.ForeignKey(Place)
    photo = models.ForeignKey(Image)
    def __unicode__(self):
        return 'Picture: ' + self.photo + ' of ' + self.place.name

