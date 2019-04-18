from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name ='home'),
    path('admin/', admin.site.urls),
    path("blog/",include('blog.urls')),
    path("comment/",include('comment.urls')),
    path("ckeditor",include("ckeditor_uploader.urls")),
    path("user/",include('user.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

