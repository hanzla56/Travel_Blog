from django.contrib import admin
from django.urls import path
from . import views

app_name = "Blog"

urlpatterns = [
    path('', views.home_page,name='home_page'),
    path('blog_page/',views.blog_page,name='blog_page'),
    path('blog_detail/<slug:slug>/',views.blog_detail,name='blog_detail'),
    path('add_comment/',views.add_comment,name='add_comment'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('category/<slug:slug>/', views.blog_by_category, name='blog_by_category'),
    path('destination/<str:destination_name>/', views.blog_by_destination, name='blog_by_destination'),
]