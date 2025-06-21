# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsArticleView.as_view(), name='news-list'),
    path('news/<int:article_id>/', views.NewsArticleView.as_view(), name='news-detail'),

    path('images/', views.ImageView.as_view(), name='image-list'),
    path('images/<int:media_id>/', views.ImageView.as_view(), name='image-detail'),

    path('videos/', views.VideoView.as_view(), name='video-list'),
    path('videos/<int:media_id>/', views.VideoView.as_view(), name='video-detail'),

    path('pdfs/', views.PdfView.as_view(), name='pdf-list'),
    path('pdfs/<int:media_id>/', views.PdfView.as_view(), name='pdf-detail'),
]