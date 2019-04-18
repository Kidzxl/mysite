from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    #http:localhost:8000/blog/1
    path("",blog_list,name = "blog_list"),
    path("<int:blog_pk>",blog_detail,name = "blog_detail"),
    path('type/<int:blog_type_pk>',blogs_with_type,name = "blogs_with_type"),
    path('dete/<int:year>/<int:month>',blogs_with_date,name ="blogs_with_date")
]
