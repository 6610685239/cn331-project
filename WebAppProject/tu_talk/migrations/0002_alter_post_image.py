# Generated by Django 5.1.1 on 2024-11-16 00:41

import tu_talk.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tu_talk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/images/', validators=[tu_talk.models.validate_image_extension]),
        ),
    ]
