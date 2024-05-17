from rest_framework import serializers
from .models import *


class PostListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields=('user')

# class PostSerializers(serializers.ModelSerializer):
#     class CommentSerializers(serializers.ModelSerializer):
#         class Meta:
#             model = Comment
#             fields = 

#     class Meta:
#         model = Post
    