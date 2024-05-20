from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_list),
    path('post/create/', views.post_create),
    path('post/<int:post_pk>/', views.post_detail),
    path('post/<int:post_pk>/edit/', views.post_detail_edit),
    path('post/<int:post_pk>/comment/', views.comment),
    path('post/<int:post_pk>/comment/create/', views.comment_create),
    path('post/<int:post_pk>/comment/<int:comment_pk>/', views.comment_edit),
]
