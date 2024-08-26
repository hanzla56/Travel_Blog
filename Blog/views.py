from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os


# Create your views here.
def home_page(request):
      carousel = Slider.objects.all()
      about_content = AboutUs.objects.first()
      latest_posts = BlogPost.objects.order_by('-published_date')[:5]
      print(f'this is latest post {latest_posts}')
      popular_guides = BlogPost.objects.filter(is_popular_guide=True)
      featured_destinations = Destination.objects.filter(is_featured_destination=True)
      first_four_destinations = featured_destinations[:4]
      remaining_destinations = featured_destinations[4:]
      
      context = {
            'carousel':carousel,
            'about':about_content,
            'latest_posts': latest_posts,
            'popular_guides': popular_guides,
            'featured_destinations': featured_destinations,
            'first_four_destinations': first_four_destinations,
            'remaining_destinations': remaining_destinations,
      }
      
      return render(request,'Blog/home.html',context)
  
def blog_page(request):
    blog_list = BlogPost.objects.all()
    print(f'this is blog list {blog_list}')
    paginator = Paginator(blog_list, 5)  # Show 10 blogs per page

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        page_obj = paginator.page(paginator.num_pages)
    
    print(f'this is page object {page_obj}')
    background_image = BlogPageBackgroundImage.objects.first()
    context = {
        'page_obj': page_obj,  # Pass page_obj to the context
        'background_image': background_image,
    }
    return render(request, 'Blog/blog.html', context)



def blog_detail(request,slug):
      blog = get_object_or_404(BlogPost,slug=slug)
      popular_guides = BlogPost.objects.filter(is_popular_guide=True)
      background_image = BlogPageBackgroundImage.objects.first()
      comments = Comment.objects.filter(post = blog)
      print('view runs here')
      context = {
            'blog':blog,
            'popular_guides':popular_guides,
            'background_image':background_image,
            'comments':comments
      }
      return render(request,'Blog/blog_detail.html',context)
  
  
def search(request):
    query = request.GET.get('query')
    
    if query:
        blogs = BlogPost.objects.filter(title__icontains=query)
    else:
        blogs = BlogPost.objects.none()  # No results if no query

    paginator = Paginator(blogs, 4)  # Show 10 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Simplified handling

    background_image = BlogPageBackgroundImage.objects.first()
    
    context = {
        'blogs':blogs,
        'page_obj': page_obj,  # Pass page_obj to the context
        'query': query,
        'is_search': bool(query),  # Set is_search based on whether there is a query
        'background_image': background_image,
    }
    
    return render(request, 'Blog/blog.html', context)
    
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
    page_obj = BlogPost.objects.filter(category=cate)
    context = {
        'heading': slug,
        'page_obj': page_obj,  # Replace with actual blog fetching logic
        'background_image':background_image,
    }
    return render(request, 'Blog/blog.html', context)

def blog_by_destination(request, slug):
    # Fetch blogs based on the destination (logic not shown here)
    dest = get_object_or_404(Destination, slug=slug)
    background_image = BlogPageBackgroundImage.objects.first()
    page_obj = BlogPost.objects.filter(destination=dest)
    context = {
        'heading': slug,
        'background_image':background_image,
        'page_obj': page_obj,  # Replace with actual blog fetching logic
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

   
def emailNewsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        obj = EmailNewsletter(email=email)
        obj.save()
        
    return JsonResponse({'message':'added successfully'})
