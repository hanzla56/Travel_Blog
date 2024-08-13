from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from tinymce import models as tinymce_models
from tinymce.models import HTMLField


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

# Destination Model
class Destination(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_destinations', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Destinations'

# Slider Model
class Slider(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sliders/')

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError('There is already an AboutUs instance. Only one instance is allowed.')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'About Us'
  
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True)
    content = tinymce_models.HTMLField()
    published_date = models.DateTimeField(auto_now_add=True)
    is_featured_destination = models.BooleanField(default=False)
    is_popular_guide = models.BooleanField(default=False)
    featured_image = models.ForeignKey('BlogPostImage', related_name='featured_image', null=True, blank=True, on_delete=models.SET_NULL)
    popular_image = models.ForeignKey('BlogPostImage', related_name='popular_image', null=True, blank=True, on_delete=models.SET_NULL)
    main_image = models.ImageField()
    category = models.ForeignKey(Category, null=True,blank=True, on_delete=models.CASCADE, related_name='blog_posts')
    destination = models.ForeignKey(Destination, null=True,blank=True, on_delete=models.CASCADE, related_name='blog_posts_destination')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogPostImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    is_featured = models.BooleanField(default=False)  # Mark image as featured if needed

    def __str__(self):
        return f"Image for {self.blog_post.title}"    
    
class BlogPageBackgroundImage(models.Model):
    image = models.ImageField(upload_to='blog_images/')
    
    def save(self, *args, **kwargs):
        if not self.pk and BlogPageBackgroundImage.objects.exists():
            raise ValidationError('There is already a Background Image instance. Only one instance is allowed.')
        return super().save(*args, **kwargs)
    
    
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    def children(self):
        """Returns replies to the comment."""
        return self.replies.all()

    @property
    def is_reply(self):
        """Returns True if this comment is a reply to another comment."""
        return self.parent is not None
    
    
    
class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    business_hours = models.CharField(max_length=100)
    

    def __str__(self):
        return f"Contact Info"
    
    def save(self, *args, **kwargs):
        if not self.pk and ContactInfo.objects.exists():
            raise ValidationError('There is already an Contactinfo instance. Only one instance is allowed.')
        return super().save(*args, **kwargs)
    
    
    
    
class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    
