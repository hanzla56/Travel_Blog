from django.contrib import admin
from .models import Category,EmailNewsletter,Destination, Slider,AboutUs,BlogPost,BlogPostImage,Comment,ContactFormSubmission,ContactInfo,BlogPageBackgroundImage
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from django.db import models

class AboutUsAdminForm(ModelForm):
    def clean(self):
        if not self.instance.pk and AboutUs.objects.exists():
            raise ValidationError('There is already an AboutUs instance. Only one instance is allowed.')
        return super().clean()

class BackgroundImageAdminForm(ModelForm):
    def clean(self):
        if not self.instance.pk and BlogPageBackgroundImage.objects.exists():
            raise ValidationError('There is already a Backgroundimage instance. Only one instance is allowed.')
        return super().clean()

class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsAdminForm
    
class BackgroundImageAdmin(admin.ModelAdmin):
    form = BackgroundImageAdminForm
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title',)
    
class BlogPostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={
            'image_class_list': [
                {'title': 'Responsive Image', 'value': 'your-custom-class'},
            ],
            'image_advtab': True,  # Optional: Show the "Advanced" tab in the image dialog
        })},
    }
    
    list_display = ('title','published_date', 'is_popular_guide','category')
    search_fields = ('title','is_featured_destination','is_popular_guide')
    list_filter = ["is_popular_guide"]
    
    # class Media:
    #     js = ('tinymce/tinymce.min.js',)
    #     css = {
    #         'all': ('tinymce/skins/ui/oxide/skin.min.css',)
    #     }
    # class Media:
    #     js= ('tinyInject.js',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(BlogPostImage)
admin.site.register(Comment)
admin.site.register(EmailNewsletter)
admin.site.register(ContactInfo)
admin.site.register(ContactFormSubmission)
admin.site.register(BlogPageBackgroundImage,BackgroundImageAdmin)

