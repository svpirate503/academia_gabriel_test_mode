# Generated by Django 5.0.3 on 2024-04-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_store', '0004_stripecustomer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripecustomer',
            name='customer_email',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
