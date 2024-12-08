from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from drf_extra_fields.fields import Base64ImageField
from posts.models import Comment, Post, Like


#Вывод комментариев (не все поля)
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_at',)

#Создание комментариев
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author','id','created_at',)

#Лайки
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('author',)

#Публикации
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='commented_post')
    likes_count = SerializerMethodField()
    image = Base64ImageField(required=False)

    def get_likes_count(self, post):
        likes = post.liked_post.count()
        return likes

    class Meta:
        model = Post
        fields = ('id', 'owner', 'text', 'image', 'created_at', 'comments','likes_count',)
        read_only_fields = ('id', 'owner', 'created_at',)