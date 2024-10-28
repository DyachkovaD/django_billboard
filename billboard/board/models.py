from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field



class Post(models.Model):
    CATEGORIES = [('tank', 'Танки'),
                  ('heal', 'Хилы'),
                  ('damager', 'ДД'),
                  ('retailer', 'Торговцы'),
                  ('guildmaster', 'Гилдмастеры'),
                  ('questgiver', 'Квестгиверы'),
                  ('blacksmith', 'Кузнецы'),
                  ('tanner', 'Кожевники'),
                  ('poitionmaster', 'Зельевары'),
                  ('spellmaster', 'Мастера заклинаний')]

    title = models.CharField(verbose_name='Заголовок', max_length=255, null=False)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE)
    category = models.CharField(verbose_name='Категория', max_length=50, choices=CATEGORIES, default=None)
    date = models.DateTimeField(auto_now_add=True)
    content = CKEditor5Field(verbose_name='Текст', config_name='extends', blank=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    author = models.OneToOneField(verbose_name='Автор', to=User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


