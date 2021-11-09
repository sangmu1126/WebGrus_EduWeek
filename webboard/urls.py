from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('create/', views.create, name='post-create'),
    path('update/', views.update, name='post-update'),
    path('detail/', views.detail, name='post-detail'),
    path('post/<int:id>/delete/', views.delete, name='post-delete'),

    path('post/<int:id>/', views.detail, name='post-detail'),
    path('post/<int:post_id>/comment/create/', views.comment_create, name='comment-create'),
    path('post/<int:post_id>/comment/delete/<int:comment_id>', views.comment_delete, name='comment-delete'),
]
