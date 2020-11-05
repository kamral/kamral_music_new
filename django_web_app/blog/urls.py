from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostApiView,
    PostDetailApiView,
    UserListApivView,
    UserDetailApiView
)
from . import views
from .serializers import UserSerializer

urlpatterns = [
    # по данной ссылке localhost:8000-
    # мы открываем все посты которые у нас есть на главной странице.
    path('', PostListView.as_view(), name='blog-home'),
    # По данной ссылку мы обращаемся к конкретному
    # пользователю. И у нас показывают все посты созданные им.
    path('user/<str:username>/', UserPostListView.as_view(),
         name='user-posts'),
    # по данной ссылке мы переходим на
    # конкретный пост
    path('post/<int:pk>/', PostDetailView.as_view(),
         name='post-detail'),
    path('post/new/', PostCreateView.as_view(),
         name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),
         name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),
         name='post-delete'),
    path('media/Files/<int:pk>',PostDeleteView.as_view(),
         name='post-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='blog-about'),
    #rest_framework
    path('api/v1/',PostApiView.as_view()),
    path('api/v1/<int:pk>/',PostDetailApiView.as_view()),
    path('users/', UserListApivView.as_view()),
    path('users/<int:pk>/',UserDetailApiView.as_view()),
]
