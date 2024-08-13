# Generated by Django 5.0.7 on 2024-08-08 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_rename_latest_image_blogpost_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='main_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latest_image', to='Blog.blogpostimage'),
        ),
    ]
