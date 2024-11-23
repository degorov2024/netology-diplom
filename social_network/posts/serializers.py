from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from posts.models import Comment, Post, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'created_at',)
#        fields = (author, text, created_at,)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='commented_post')
    likes_count = SerializerMethodField()

    def get_likes_count(self, post):
        likes = post.liked_post.count()
        return likes

    class Meta:
        model = Post
        fields = ('id', 'text', 'image', 'created_at', 'comments','likes_count')
        # fields = (id, owner, text, image, created_at, comments,'likes_count')