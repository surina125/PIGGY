from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class CommentSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)

        class Meta:
            model = Comment
            fields = '__all__'

    comment_set = CommentSerializer(many=True, read_only=True)
    formatted_created_at = serializers.SerializerMethodField()  

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'formatted_created_at', 'comment_set']

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    
class CommentSerialzer(serializers.ModelSerializer):
    class PostListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'
            read_only_fields = ('user',)
    user = UserSerializer(read_only=True)
    post = PostListSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y.%m.%d. %H:%M', read_only=True)


    class Meta:
        model = Comment
        fields = '__all__'