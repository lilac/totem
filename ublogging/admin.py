from ublogging.models import *
from django.contrib import admin


admin.site.register(Profile)
admin.site.register(Post)

models = [Image, Place, PlaceFollower, CheckIn, PlaceComment, PostComment,
          CheckInComment, Mail, PhotoGallery, PlacePicture]

admin.site.register(models)