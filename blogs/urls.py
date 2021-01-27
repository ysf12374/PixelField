from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import StreamingHttpResponse

urlpatterns = [
    path('api/v1/pixelblog/login', views.login, name='login'),
    path('api/v1/pixelblog/category', views.category, name='category'),
    path('api/v1/pixelblog/tag', views.tag, name='tag'),
    path('api/v1/pixelblog/blog', views.blog, name='blog'),
    path('api/v1/pixelblog/user', views.user, name='user'),
    path('api/v1/pixelblog/comment', views.comment, name='comment'),
    path('api/v1/pixelblog/content', views.content, name='content'),
]

 
