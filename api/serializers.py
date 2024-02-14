from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'user', 'date_created', 'markdown', 'url')


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User  # draws from existing model
        fields = ['id', 'username', 'password', 'email']
