from contrib.karma.models import (Karma, KarmaSweet,
                                  Vote, Log)
from contrib.privatetimeline.models import PrivateSweet
from django.contrib import admin


class KarmaAdmin(admin.ModelAdmin):
    list_display = ('user', 'karma')


class KarmaSweetAdmin(admin.ModelAdmin):
    list_display = ('sweet', 'karma')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'sweet', 'vote')


class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'karma', 'updated')


class PrivateSweetAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'msg')

admin.site.register(Karma, KarmaAdmin)
admin.site.register(KarmaSweet, KarmaSweetAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(PrivateSweet, PrivateSweetAdmin)
