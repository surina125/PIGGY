from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from .serializers import *
from .models import *



# Create your views here.

# 전체 게시글 read
@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializers = PostListSerializers(posts, many=True)
        return Response(serializers.data)

# 단일 게시글 read, create, update, delete
@api_view(['GET','POST'])    
def post_detail(request, post_pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_pk)
        serializers = PostListSerializers(post, many=true)
        return Response(serializers.data)
    # elif request.method == 'POST':
    #     serializers = PostListSerializers(data=posts, many=True)
    #     if serializers.is_valid():
    #         serializers.save()



    

    
