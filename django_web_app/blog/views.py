from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve
from django.db.models import Q

from rest_framework import generics,permissions
from .serializers import PostSerializer,UserSerializer
from .permissions import IsAuthorOrReadOnly
from  django.contrib.auth import get_user_model


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


# Создаем класс для обработки созданных постов каждым пользователем.
# В качестве обработки используем файл user_posts.html
# В качестве модели Post
# Так как нам нужно посредством цикла выводить
# все посты, мы должны использовать objects_list,
# вместо это используем posts.
# Мы изменили имя цикла, посредством переменной context_object_name
# Далее мы разбиваем главную страницу на 2 поста на одной странице
#  Чтобы ограничить доступ к просмотру
# только зарегистрированным пользователям,
# Django имеет LoginRequired mixin,
# login_url='login'-переводит нас на login,
# если мы не вошли в систему.

class PostListView( LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2



# Создаем класс для обработки созданных постов каждым пользователем.
# В качестве обработки используем файл user_posts.html
# В качестве модели Post
# Так как нам нужно посредством цикла выводить
# все посты, мы должны использовать objects_list,
# вместо это используем posts.
# Мы изменили имя цикла, посредством переменной context_object_name
# Далее мы разбиваем главную страницу на 2 поста на одной странице
#  Чтобы ограничить доступ к просмотру
# только зарегистрированным пользователям,
# Django имеет LoginRequired mixin,
# login_url='login'-переводит нас на login,
# если мы не вошли в систему.
class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2


    # Вызвали функцию get_queryset- чтобы работать с базой данных.
    # Выводим все посты созданные пользователем по первичному ключу User
    # Так как User это встроенная авторизация джанго, в нее входит
    # много полей вплоть - 'username'. И мы получаем все посты от 'username'
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


    # Данный класс позволяет нам открывать
    # и прочитать конкретный пост. обрабатывая post_detail.html
    # Чтобы ограничить доступ только
    # для зарегистрированных пользователей
    # только зарегистрированным пользователям,
    # Django имеет LoginRequired mixin,
    # login_url='login'-переводит нас на login,
    # если мы не вошли в систему.
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


# Данный класс позволяет создать
# новые посты только для зарегистрированных пользователей
# Чтобы ограничить доступ к просмотру
# только зарегистрированным пользователям,
# Django имеет LoginRequired mixin,
# login_url='login'-переводит нас на login,
# если мы не вошли в систему.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    # данная функция позволяет закрепить пост
    # за кокретным пользователем который пишет.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Данный класс позволяет обновлять посты пользователя.
# Чтобы ограничить доступ к просмотру
# только зарегистрированным пользователям,
# Django имеет LoginRequired mixin,
# login_url='login'-переводит нас на login,
# если мы не вошли в систему.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    # данная функция позволяет закрепить пост
    # за кокретным пользователем который пишет.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
# Данный класс позволяет пост  пользователя.
# Чтобы ограничить доступ к просмотру
# только зарегистрированным пользователям,
# Django имеет LoginRequired mixin,
# login_url='login'-переводит нас на login,
# если мы не вошли в систему.

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # после удаления поста перенаправляем на
    # locahost:8000
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'


    # данная функция позволяет закрепить пост
    # за кокретным пользователем который пишет.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# Данный класс позволяет чиать и записывать
# благодаря ListCreateAPIView-вызванный из библиотеки generics

class PostApiView(generics.ListCreateAPIView):
    #откроем все записи с помощью создание
    # экземдяра класса queryset-в которую вложим Post.objects.all()-
    # для показа всех записей
    queryset = Post.objects.all()
    # для работы с api- создадим также экземляр класса
    # serializer_class,в которую присвоим PostSerializer
    serializer_class = PostSerializer


# Данный класс разбирает каждый пост индивидуально
# С помощью пакета-RetrieveUpdateDestroyAPIView-
# мы сможем кажду запись читать, удалять и обновлять
class PostDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    # откроем все записи с помощью создание
    # экземдяра класса queryset-в которую вложим Post.objects.all()-
    # для показа всех записей
    queryset = Post.objects.all()
    # для работы с api- создадим экземпляр класса
    # serializer_class, и присвоим ему PostSerializer
    serializer_class = PostSerializer

# класс UserList, в котором перечислены все пользователи
# Данный класс позволяет чиать и записывать
# благодаря ListCreateAPIView-вызванный из библиотеки generics

class UserListApivView(generics.ListCreateAPIView):

    # Нам нужно также ссылаться на модель пользователей
    # через get_user_model

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

# класс UserDetail, предоставляющий подробное
# представление отдельного пользователя.

class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer






