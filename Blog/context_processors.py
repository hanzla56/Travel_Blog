from .models import Category, Destination, Slider,BlogPost,BlogPageBackgroundImage
from django.shortcuts import render
from django.core.paginator import Paginator

def common_data(request):
    categories = Category.objects.filter(parent__isnull=True)
    
    print(f'this is category {categories}')
    destinations = Destination.objects.filter(parent__isnull=True)
    sliders = Slider.objects.all()
    return {
        'categories': categories,
        'destinations': destinations,
        'sliders': sliders,
    }

def search(request):
    query = request.GET.get('query')  # Corrected to 'GET' instead of 'Get'
    
    blogs = BlogPost.objects.filter(title__icontains=query) if query else BlogPost.objects.none()
    is_search = True 
    
    paginator = Paginator(blogs, 10)  # Show 10 blog posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    background_image = BlogPageBackgroundImage.objects.first()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'is_search':is_search,
        'background_image': background_image,
    }
    
    return render(request, 'Blog/blog.html', context)
    