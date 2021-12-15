from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import Game, PlayList, Review, WatchListItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['token', 'username', 'password']


class WatchListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListItem
        fields = ['id', 'playlist', 'user']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'game_db_url']


class ReviewSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rating': instance.rating,
            'review_text': instance.review_text,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'user': {
                'username': instance.user.username
            }
        }

    class Meta:
        model = Review
        fields = ['id', 'rating', 'review_text', 'created_at',
                  'updated_at', 'playlist', 'user']


class PlayListSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = PlayList
        fields = ['id', 'name', 'creator', 'description',
                  'content_type', 'youtube_url', 'game', 'reviews']
