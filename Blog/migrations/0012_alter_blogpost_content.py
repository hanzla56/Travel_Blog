# Generated by Django 5.0.7 on 2024-08-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0011_alter_blogpost_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(),
        ),
    ]
