from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    # Отношение один к одному предполагает,
    # что одна строка из одной таблицы может быть связана только с одной сущностью
    # из другой таблицы. Например, пользователь может иметь какие-либо данные,
    # которые описывают его учетные данные.
    # Всю базовую информацию о пользователе, типа имени, возраста,
    # можно выделить в одну модель, а учетные данные - логин, пароль,
    # время последнего входа в систему,
    # количество неудачных входов и т.д. - в другую модель:
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # расширение ImageField-позволяет загрузить фото,
    # default-по умолчанию ставит фото выбранное нами,
    # upload_to=' '- создает репозиторий в котором мы
    # можем хранить наши фото
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Уменьшаем изображение и размер
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        # Выбор картинки
        img = Image.open(self.image.path)
        # Условие
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
