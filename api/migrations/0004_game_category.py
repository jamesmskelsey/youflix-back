# Generated by Django 3.2.9 on 2021-12-21 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_playlist_cover_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='category',
            field=models.CharField(default='Souls-like', max_length=255),
            preserve_default=False,
        ),
    ]