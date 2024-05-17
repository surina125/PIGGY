from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list),
    path('post/<int:post_pk>/', views.post_detail),
    path('post/<int:post_pk>/comment/', views.comment_create),
    path('post/<int:post_pk>/comment/<int:comment_pk>/', views.comment_edit),
]
