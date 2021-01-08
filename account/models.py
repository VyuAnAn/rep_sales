from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    """ Расширенный профиль пользователя """
    is_activated = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Признак, прошел ли пользователь активацию?")

    send_messages = models.BooleanField(
        default=True,
        verbose_name="Отправка уведомлений")

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения")

    phone_number = models.CharField(
        max_length=16,
        null=True,
        verbose_name="Номер телефона")

    # photo = models.ImageField(
    #     upload_to='users/%Y/%m/%d/',
    #     blank=True,
    #     verbose_name="Изображение")

    class Meta(AbstractUser.Meta):
        pass
