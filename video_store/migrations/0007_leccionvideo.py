# Generated by Django 5.0.3 on 2024-04-27 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_store', '0006_categoria_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeccionVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('url_video', models.URLField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecciones_video', to='video_store.post')),
            ],
        ),
    ]
