from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostSerializer

class AllPostView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class CommentView(APIView):
    def get(self, request, *args, **kwargs):
        pass

class PostAPI(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        the_post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(instance=the_post, many=False)
        return Response(serializer.data)

    #создание новой публикации
    def post(self, request, *args, **kwargs):
        data=request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Публикация создана"})

    #изменение существующей публикации
    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return Response({"message": "Публикация удалена"})
        except Post.DoesNotExist:
            return Response({"message": "Публикация не найдена"},
                            status=status.HTTP_404_NOT_FOUND)