from django.contrib import admin
from .models import Game, PlayList, WatchListItem, Review

admin.site.register(Game)
admin.site.register(PlayList)
admin.site.register(WatchListItem)
admin.site.register(Review)
