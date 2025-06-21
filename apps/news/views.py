# views.py
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser
from .models import NewsArticle, NewImage, NewVideo, NewsPdf
from .serializers import NewsArticleSerializer, NewImageSerializer, NewVideoSerializer, NewsPdfSerializer
from Damnhour.shortcuts import get_object_or_404, IsAuth, has_permission
from Damnhour.pagination import StandardResultsSetPagination


class NewsArticleView(APIView):
    parser_classes = (MultiPartParser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['ar_new_type', 'en_new_type', 'is_active']
    search_fields = [
        'ar_title', 'en_title',
        'ar_content', 'en_content',
        'ar_keywords', 'en_keywords'
    ]

    def get_queryset(self):
        queryset = NewsArticle.objects.all()

        # Custom keyword filter
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            queryset = queryset.filter(
                Q(ar_keywords__icontains=keyword) |
                Q(en_keywords__icontains=keyword))

        return queryset.order_by('-created_at')

    def get(self, request, article_id=None):
        if article_id:
            article = get_object_or_404(NewsArticle, id=article_id)
            serializer = NewsArticleSerializer(article)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = NewsArticleSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = NewsArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not has_permission('news.create_news_article', request):
            raise PermissionDenied()

        serializer = NewsArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, article_id):
        article = get_object_or_404(NewsArticle, id=article_id)
        if not has_permission('news.change_news_article', request):
            raise PermissionDenied()

        serializer = NewsArticleSerializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, article_id):
        article = get_object_or_404(NewsArticle, id=article_id)
        if not has_permission('news.delete_news_article', request):
            raise PermissionDenied()

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaView(APIView):
    parser_classes = (MultiPartParser,)

    def get_model(self):
        raise NotImplementedError

    def get_serializer(self):
        raise NotImplementedError

    def get(self, request, media_id=None, article_id=None):
        if media_id:
            media = get_object_or_404(self.get_model(), id=media_id)
            return Response(self.get_serializer()(media).data)

        if article_id:
            media = self.get_model().objects.filter(news_article_id=article_id)
            return Response(self.get_serializer()(media, many=True).data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.get_serializer()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, media_id):
        media = get_object_or_404(self.get_model(), id=media_id)
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageView(MediaView):
    def get_model(self):
        return NewImage

    def get_serializer(self):
        return NewImageSerializer


class VideoView(MediaView):
    def get_model(self):
        return NewVideo

    def get_serializer(self):
        return NewVideoSerializer


class PdfView(MediaView):
    def get_model(self):
        return NewsPdf

    def get_serializer(self):
        return NewsPdfSerializer