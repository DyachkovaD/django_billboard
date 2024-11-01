from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, send_mail
from board.models import *
from account.models import *
from account.views import generate_string
from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User


@receiver(post_save, sender=get_user_model(), )
def new_user_code(sender, instance, **kwargs):
    new_code = OneTimeCode.objects.create(user=instance,
                                  code=generate_string(6))
    new_code.save()

    message = f'Ваш код авторизации на форуме: \n' \
              f'{new_code.code}'
    send_mail(
        f'Код авторизации пользователя',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email],
    )


@receiver(post_save, sender=Reply, )
def notify_author_new_reply(sender, instance, **kwargs):
    subject = f'Новый отклик к вашему объявлению!'

    message = f'К вашему объявлению {instance.post}: новый отклик!'
    send_mail(
        f'Отклик на объявление',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.post__author.email],
    )