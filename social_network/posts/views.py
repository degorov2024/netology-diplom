from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from posts.models import Post, Like, Comment
from posts.serializers import (PostSerializer, CommentSerializer,
                               CommentCreateSerializer, LikeSerializer)

import os


#Удаление изображения с сервера (на вход даётся объект Post)
def delete_image(post):
    if post.image:
        if os.path.isfile(post.image.path):
            os.remove(post.image.path)


class AllPostView(APIView):
    """Просмотр всех постов"""
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostCreate(APIView):
    """Создание новой публикации. Текст и картинка опциональны.
    В теле запроса application/json, причём изображение в формате Base64. """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data=request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
            return Response({"message": "Публикация создана"})

class PostAPI(APIView):
    """Просмотр, редактирование и удаление публикаций по id"""
    #GET-запросы работают у всех, остальные же - только у авторизованных пользователей
    permission_classes = [IsAuthenticatedOrReadOnly]

    #Просмотр данных поста по его id
    def get(self, request, post_id):
        the_post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(instance=the_post, many=False)
        return Response(serializer.data)

    #Изменение существующей публикации. В запросе JSON, картинка в формате Base64.
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            data = request.data
            #проверка на то, является ли пользователь автором поста (403, если нет)
            if post.owner == self.request.user:
                serializer = PostSerializer(post, data=data)
                if serializer.is_valid():
                    #если поменялась картинка, то старая удаляется с сервера
                    if data['image']:
                        delete_image(post)
                    serializer.save()
                    return Response({"message": "Публикация отредактирована"})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"message": "Публикация не найдена"},
                            status=status.HTTP_404_NOT_FOUND)

    #Удаление публикации
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            #проверка на то, является ли пользователь автором поста (403, если нет)
            if post.owner == self.request.user:
                #если к посту прикреплена картинка, то файл удаляется с сервера
                delete_image(post)
                post.delete()
                return Response({"message": "Публикация удалена"})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"message": "Публикация не найдена"},
                            status=status.HTTP_404_NOT_FOUND)


class CommentAPI(APIView):
    """Cоздание и удаление комментариев (по id поста и комментария соответственно)"""
    permission_classes = [IsAuthenticated]

    #создание комментария авторизованным пользователем (запрос application/json)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user)
            return Response({"message": "Комментарий опубликован"})

    #удаление комментария по id комментария (может только автор комментария)
    def delete(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
            #проверка на то, автор ли комментария текущий пользователь (403, если нет)
            if comment.author == self.request.user:
                comment.delete()
                return Response({"message": "Комментарий удалён"})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist:
            return Response({"message": "Такого комментария не существует"},
                            status=status.HTTP_404_NOT_FOUND)


class LikeAPI(APIView):
    """Возможность ставить и удалять лайки"""
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        #Проверка, был ли поставлен лайк до этого
        if (Like.objects.filter(post=post_id) &
            Like.objects.filter(author=self.request.user)).first():
            return Response({"message": "Лайк уже был поставлен ранее"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = LikeSerializer(data={"post":post_id})
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=self.request.user)
                return Response({"message": "Лайк поставлен"})

    def delete (self, request, post_id):
        try:
            like = Like.objects.get(post=post_id, author=self.request.user)
            like.delete()
            return Response({"message": "Лайк удалён"})
        except Like.DoesNotExist:
            return Response({"message": "Лайк не найден"},
                            status=status.HTTP_404_NOT_FOUND)