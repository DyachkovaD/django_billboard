# Generated by Django 5.1.2 on 2024-10-29 13:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('board', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('category', models.CharField(choices=[('tank', 'Танки'), ('heal', 'Хилы'), ('damager', 'ДД'), ('retailer', 'Торговцы'), ('guildmaster', 'Гилдмастеры'), ('questgiver', 'Квестгиверы'), ('blacksmith', 'Кузнецы'), ('tanner', 'Кожевники'), ('poitionmaster', 'Зельевары'), ('spellmaster', 'Мастера заклинаний')], default=None, max_length=50, verbose_name='Категория')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(verbose_name='Текст')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
        ),
    ]
