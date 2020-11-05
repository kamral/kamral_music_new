from rest_framework import serializers
from .models import Post
# Нам нужно импортировать пользовательскую модель,
# Стоит отметить, что хотя мы использовали
# get_user_model для ссылки на модель пользователя
# здесь, на самом деле существует три
# различных способа ссылки на модель пользователя в Django.
# Используя get_user_model, мы гарантируем,
# что имеем в виду правильную модель пользователя,
# будь то пользователь по умолчанию или
# пользовательская модель пользователя, как это часто
# определяется в новых проектах Django.
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):

    class Meta:

        fields=('id','title', 'file','content','author')
        model=Post

# • новый класс сериализатора для модели
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # Используя get_user_model, мы гарантируем,
        # что имеем в виду правильную модель пользователя,
        # будь то пользователь по умолчанию или
        # пользовательская модель пользователя, как это часто
        # определяется в новых проектах Django.
        model=get_user_model()
        fields=('id','username')

