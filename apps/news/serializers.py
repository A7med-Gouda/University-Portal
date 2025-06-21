# serializers.py
from rest_framework import serializers
from bleach import clean
from .models import NewsArticle, NewImage, NewVideo, NewsPdf


class MediaSerializerMixin:
    def create_media(self, instance, media_data, model_class):
        for media in media_data:
            model_class.objects.create(news_article=instance, **{model_class._meta.get_field('file_field').name: media})


class NewsArticleSerializer(MediaSerializerMixin, serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=None, use_url=False),
        write_only=True,
        required=False
    )
    videos = serializers.ListField(
        child=serializers.FileField(max_length=None, use_url=False),
        write_only=True,
        required=False
    )
    pdfs = serializers.ListField(
        child=serializers.FileField(max_length=None, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = NewsArticle
        fields = '__all__'
        extra_kwargs = {
            'ar_content': {'allow_blank': True},
            'en_content': {'allow_blank': True}
        }

    def validate(self, data):
        data['ar_content'] = clean(data.get('ar_content', ''))
        data['en_content'] = clean(data.get('en_content', ''))
        return data

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        videos = validated_data.pop('videos', [])
        pdfs = validated_data.pop('pdfs', [])

        article = super().create(validated_data)

        self.create_media(article, images, NewImage)
        self.create_media(article, videos, NewVideo)
        self.create_media(article, pdfs, NewsPdf)

        return article


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ['id', 'file', 'created_at']


class NewImageSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = NewImage
        fields = MediaSerializer.Meta.fields + ['image']


class NewVideoSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = NewVideo
        fields = MediaSerializer.Meta.fields + ['video']


class NewsPdfSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = NewsPdf
        fields = MediaSerializer.Meta.fields + ['pdf']