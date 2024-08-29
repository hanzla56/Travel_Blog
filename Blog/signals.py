# signals.py
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Destination, Slider, AboutUs, BlogPostImage, BlogPageBackgroundImage, BlogPost
import os
import logging

logger = logging.getLogger(__name__)

def delete_file(file_path):
    if file_path and os.path.isfile(file_path):
        try:
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
    else:
        logger.warning(f"File not found: {file_path}")

def handle_image_update(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            delete_file(old_instance.image.path)

@receiver(pre_save, sender=Destination)
def update_destination_image(sender, instance, **kwargs):
    handle_image_update(sender, instance, **kwargs)

@receiver(pre_save, sender=Slider)
def update_slider_image(sender, instance, **kwargs):
    handle_image_update(sender, instance, **kwargs)

@receiver(pre_save, sender=AboutUs)
def update_about_us_image(sender, instance, **kwargs):
    handle_image_update(sender, instance, **kwargs)

@receiver(pre_save, sender=BlogPostImage)
def update_blog_post_image(sender, instance, **kwargs):
    handle_image_update(sender, instance, **kwargs)

@receiver(pre_save, sender=BlogPageBackgroundImage)
def update_blog_page_background_image(sender, instance, **kwargs):
    handle_image_update(sender, instance, **kwargs)

@receiver(pre_save, sender=BlogPost)
def update_blog_post_main_image(sender, instance, **kwargs):
    handle_image_update(sender, instance, **kwargs)

@receiver(post_delete, sender=Destination)
def delete_destination_image(sender, instance, **kwargs):
    if instance.image:
        delete_file(instance.image.path)

@receiver(post_delete, sender=Slider)
def delete_slider_image(sender, instance, **kwargs):
    if instance.image:
        delete_file(instance.image.path)

@receiver(post_delete, sender=AboutUs)
def delete_about_us_image(sender, instance, **kwargs):
    if instance.image:
        delete_file(instance.image.path)

@receiver(post_delete, sender=BlogPostImage)
def delete_blog_post_image(sender, instance, **kwargs):
    if instance.image:
        delete_file(instance.image.path)

@receiver(post_delete, sender=BlogPageBackgroundImage)
def delete_blog_page_background_image(sender, instance, **kwargs):
    if instance.image:
        delete_file(instance.image.path)

@receiver(post_delete, sender=BlogPost)
def delete_blog_post_main_image(sender, instance, **kwargs):
    if instance.main_image:
        delete_file(instance.main_image.path)
