# Generated by Django 5.1.2 on 2024-11-02 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_reply_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
