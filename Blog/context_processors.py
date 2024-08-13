from .models import Category, Destination, Slider

def common_data(request):
    categories = Category.objects.filter(parent__isnull=True, blog_posts__isnull=False)
    
    print(f'this is category {categories}')
    destinations = Destination.objects.filter(parent__isnull=True)
    sliders = Slider.objects.all()
    return {
        'categories': categories,
        'destinations': destinations,
        'sliders': sliders,
    }
