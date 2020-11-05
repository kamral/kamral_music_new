"""django_web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

# LoginView-Отображает форму авторизации и обрабатывает действия с ней.
# LogoutView-Выводит пользователя из системы
# и отображает сообщение "Вы вышли из системы".
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # регистрация пользователя
    path('login/', LoginView.as_view
    (template_name='users/login.html'), name='login'),
    # авторизация на сайт
    path('register/', user_views.register, name='register'),
    #профиль пользователя
    path('profile/', user_views.profile, name='profile'),

    # Выводит пользователя из системы и
    # отображает сообщение "Вы вышли из системы"
    path('logout/', LogoutView.as_view
    (template_name='users/logout.html'), name='logout'),

    path('', include('blog.urls')),
    path('', include('blog.urls')),
    path('/api-auth/',include('rest_framework.urls')),
    # Login and Logout
    path('api/v1/rest-auth/',include('rest_auth.urls')),
    # registrations
    path('api/v1/rest-auth/registration/',
         include('rest_auth.registration.urls')),


]

#мы вызываем settings.DEBUG , для работы с медиа файлами
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)