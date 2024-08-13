from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os


# Create your views here.
def home_page(request):
      carousel = Slider.objects.all()
      about_content = AboutUs.objects.first()
      latest_posts = BlogPost.objects.order_by('-published_date')[:5]
      popular_guides = BlogPost.objects.filter(is_popular_guide=True)
      featured_destinations = BlogPost.objects.filter(is_featured_destination=True)
      
      context = {
            'carousel':carousel,
            'about':about_content,
            'latest_posts': latest_posts,
            'popular_guides': popular_guides,
            'featured_destinations': featured_destinations,
      }
      
      return render(request,'Blog/home.html',context)

def blog_page(request):
      blogs = BlogPost.objects.all()
      background_image = BlogPageBackgroundImage.objects.first()
      context = {
            'blogs':blogs,
      }
      return render(request,'Blog/blog.html',context)

def blog_detail(request,slug):
      blog = get_object_or_404(BlogPost,slug=slug)
      popular_guides = BlogPost.objects.filter(is_popular_guide=True)
      background_image = BlogPageBackgroundImage.objects.first()
      comments = Comment.objects.filter(post = blog)
      context = {
            'blog':blog,
            'popular_guides':popular_guides,
            'background_image':background_image,
            'comments':comments
      }
      return render(request,'Blog/blog_detail.html',context)

def about(request):
      about_content = AboutUs.objects.first()
      context ={
            'about':about_content
      }
      return render(request,'Blog/about.html',context)

def contact(request):
    if request.method == 'GET':
        c_info = ContactInfo.objects.first()
        context = {
            'c_info': c_info,
        }
        return render(request, 'Blog/contact.html', context)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name or not email or not message:
            # Add an error message
            messages.error(request, 'Please fill in all required fields.')
            # Redirect back to the contact page
            return redirect('contact')  # Replace 'contact' with your URL name if different
        
        # Save the form data
        ContactFormSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        # Add a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        # Redirect back to the contact page
        return redirect('Blog:contact')  # Replace 'contact' with your URL name if different
  
  
def blog_by_category(request, slug):
    # Fetch blogs based on the category (logic not shown here)
    print(slug)
    cate = get_object_or_404(Category, slug=slug)
    background_image = BlogPageBackgroundImage.objects.first()
    blogs = BlogPost.objects.filter(category=cate)
    context = {
        'heading': slug,
        'blogs': blogs,  # Replace with actual blog fetching logic
        'background_image':background_image,
    }
    return render(request, 'Blog/blog.html', context)

def blog_by_destination(request, destination_name):
    # Fetch blogs based on the destination (logic not shown here)
    background_image = BlogPageBackgroundImage.objects.first()
    context = {
        'heading': destination_name,
        'background_image':background_image,
        'blogs': [],  # Replace with actual blog fetching logic
    }
    return render(request, 'Blog/blog.html', context)



def add_comment(request):
      post_id = request.POST.get('post_id')
      comment_text = request.POST.get('comment')
      name = request.POST.get('name')
      email = request.POST.get('email')
      comment_id = request.POST.get('comment_id')  # To check if it's a reply

      if not post_id or not comment_text or not name or not email:
        return JsonResponse({'error': 'All fields are required.'}, status=400)

      try:
        post = BlogPost.objects.get(id=post_id)
      except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Invalid post.'}, status=400)

      if comment_id:
        try:
            parent_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Invalid parent comment.'}, status=400)
        # Create reply
        comment = Comment.objects.create(
            post=post,
            comment_text=comment_text,
            name=name,
            email=email,
            parent=parent_comment  # Assuming your Comment model has a parent field
        )
      else:
        # Create a new comment
        comment = Comment.objects.create(
            post=post,
            comment_text=comment_text,
            name=name,
            email=email
        )

      comment.save()
      return JsonResponse({'message': 'Comment submitted successfully!','comment_id': comment.id }, status=200)

      return JsonResponse({'error': 'Invalid request.'}, status=400)

   
   
   
# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES.get('file')
#         if not uploaded_file:
#             return JsonResponse({'error': 'No file uploaded'}, status=400)

#         try:
#             # Define the file path where the image will be saved
#             file_path = os.path.join(settings.MEDIA_ROOT, 'blog_images', uploaded_file.name)
#             file_url = os.path.join(settings.MEDIA_URL, 'blog_images', uploaded_file.name)

#             # Create the directory if it doesn't exist
#             os.makedirs(os.path.dirname(file_path), exist_ok=True)

#             # Save the file
#             with open(file_path, 'wb+') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)

#             # Return the file URL
#             return JsonResponse({'location': file_url})

#         except Exception as e:
#             # Log the error and return a failure response
#             print(f"Error saving file: {e}")
#             return JsonResponse({'error': 'Failed to upload image'}, status=500)

#     return JsonResponse({'error': 'Invalid request'}, status=400)