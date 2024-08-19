# signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Destination, Slider, AboutUs, BlogPostImage, BlogPageBackgroundImage, BlogPost
import os

def delete_file(file_path):
    if file_path and os.path.isfile(file_path):
        os.remove(file_path)

@receiver(post_delete, sender=Destination)
def delete_destination_image(sender, instance, **kwargs):
    delete_file(instance.image.path)

@receiver(post_delete, sender=Slider)
def delete_slider_image(sender, instance, **kwargs):
    delete_file(instance.image.path)

@receiver(post_delete, sender=AboutUs)
def delete_about_us_image(sender, instance, **kwargs):
    delete_file(instance.image.path)

@receiver(post_delete, sender=BlogPostImage)
def delete_blog_post_image(sender, instance, **kwargs):
    delete_file(instance.image.path)

@receiver(post_delete, sender=BlogPageBackgroundImage)
def delete_blog_page_background_image(sender, instance, **kwargs):
    delete_file(instance.image.path)

@receiver(post_delete, sender=BlogPost)
def delete_blog_post_main_image(sender, instance, **kwargs):
    delete_file(instance.main_image.path)
