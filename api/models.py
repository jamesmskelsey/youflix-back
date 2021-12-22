from django.db.models import Model, CharField, ForeignKey
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F
from django.db.models.fields import IntegerField, TextField, DateTimeField
from django.contrib.auth.models import User


class Game(Model):
    name = CharField(max_length=255)
    game_db_url = CharField(max_length=255)
    cover_url = CharField(max_length=255)
    category = CharField(max_length=255)

    def __str__(self):
        return f"game - {self.name}"


class PlayList(Model):
    name = CharField(max_length=255)
    creator = CharField(max_length=255)
    description = TextField()
    # walkthrough/let's play/silly/boss guide
    content_type = CharField(max_length=255)
    youtube_url = CharField(max_length=255)
    cover_url = CharField(max_length=255)
    game = ForeignKey(Game, related_name='playlists', on_delete=CASCADE)

    def __str__(self):
        return f"pl - {self.name} by {self.creator}"


class Review(Model):
    rating = IntegerField()
    review_text = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    playlist = ForeignKey(PlayList, related_name='reviews', on_delete=CASCADE)
    user = ForeignKey(User, related_name='reviews', on_delete=CASCADE)

    def __str__(self):
        return f"{self.user}'s review of {self.playlist}"


class WatchListItem(Model):
    playlist = ForeignKey(
        PlayList, related_name='watchlist', on_delete=CASCADE)
    user = ForeignKey(User, related_name='watchlist', on_delete=CASCADE)

    def __str__(self):
        return f"{self.user} watching playlist {self.playlist}"
