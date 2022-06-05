from django.urls import path
from .views import *


urlpatterns = [
    path('', main, name='main'),
    path('article/<int:id>/', getItem, name='getItem'),
    path('article/category/<int:id>/', getByCategory, name='getByCategory'),
    path('videos/', getVideos, name='getVideos'),
    path('videos/category/<int:id>/', getByCategoryVideos, name='getByCategoryVideos'),
    path('search_article/', search_article, name='search_article'),
    path('search_video/', search_video, name='search_video'),
]
