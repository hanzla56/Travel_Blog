# Generated by Django 5.0.7 on 2024-08-26 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0017_remove_blogpost_is_featured_destination_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNewsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
