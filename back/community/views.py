from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *



# Create your views here.

# 전체 게시글 read, 단일 게시글 create
@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

# 단일 게시글 read, update, delete
@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])    
def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        print(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE': 
        post.delete()
        return Response('게시물이 삭제되었습니다.', status=status.HTTP_204_NO_CONTENT)

# 댓글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    serializer = CommentSerialzer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 수정, 삭제
@api_view(['PUT','DELETE'])
@permission_classes([IsAuthenticated])
def comment_edit(request, post_pk, comment_pk):
    post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerialzer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comment.delete()
        return Response('게시물이 삭제되었습니다.', status=status.HTTP_204_NO_CONTENT)
        
            







    

    
