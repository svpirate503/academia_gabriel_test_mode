# Generated by Django 5.0.3 on 2024-04-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_store', '0010_alter_leccionvideo_url_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leccionvideo',
            name='url_video',
        ),
        migrations.AddField(
            model_name='leccionvideo',
            name='url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
