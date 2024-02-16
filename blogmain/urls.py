from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeViewSet.as_view(), name='blog-home'),
    path('about/', views.AboutViewSet.as_view(), name='blog-about'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('posts/<str:username>', views.UserPostListView.as_view(), name='post-user-list')
    
]