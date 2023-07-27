from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Morph, Topic


class MorphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Morph
        fields = ['id', 'name', 'summary', 'icon', 'json_data']


class UserSerializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username']


class TopicSerializer(serializers.ModelSerializer): #HyperlinkedModelSerializer
    # morph = serializers.HyperlinkedIdentityField(view_name='api:morph-detail')
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Topic
        fields = ['id', 'name', 'summary', 'icon', 'json_data', 'morph', 'user', 'created_by', 'created_date']
