# Generated by Django 5.0.3 on 2024-04-27 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_store', '0008_alter_leccionvideo_url_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leccionvideo',
            name='url_video',
            field=models.URLField(max_length=300),
        ),
    ]
