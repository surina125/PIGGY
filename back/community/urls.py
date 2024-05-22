from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_list),                                           # 전체 게시물 조회
    path('post/create/', views.post_create),                                  # 게시물 생성
    path('post/<int:post_pk>/', views.post_detail),                           # 단일 게시물 조회
    path('post/<int:post_pk>/edit/', views.post_detail_edit),                 # 단일 게시물 수정 및 삭제
    path('post/<int:post_pk>/comment/', views.comment),                       # 댓글 조회
    path('post/<int:post_pk>/comment/create/', views.comment_create),         # 댓글 생성
    path('post/<int:post_pk>/comment/<int:comment_pk>/', views.comment_edit), # 댓글 수정 및 삭제
]
