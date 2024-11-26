from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Like
from posts.serializers import PostSerializer

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


class CommentAPI(APIView):
    """Cоздание и удаление комментариев (по id поста и комментария соответственно)"""
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class PostCreate(APIView):
    """Создание новой публикации"""
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data=request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
            return Response({"message": "Публикация создана"})

class PostAPI(APIView):
    """Просмотр, редактирование и удаление публикаций по id, а также возможность
    ставить и удалять лайки"""
    #GET-запросы работают у всех, остальные же - только у авторизованных пользователей
    permission_classes = [IsAuthenticatedOrReadOnly]

    #Просмотр данных поста по его id
    def get(self, request, post_id):
        the_post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(instance=the_post, many=False)
        return Response(serializer.data)

    #Лайки
    def put(self, request, post_id):
        #получаем объект Like либо None (исходя из того, был ли лайк уже поставлен)
        like = (Like.objects.filter(post=post_id) &
                Like.objects.filter(author=self.request.user)).first()
        post = Post.objects.get(id=post_id)
        if like:
            like = Like.objects.get(post=post)
            like.delete()
            return Response({"message": "Лайк удалён"})
        else:
            Like.objects.create(post=post, author=self.request.user)
            return Response({"message": "Лайк поставлен"})

    #Изменение существующей публикации
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            data = request.data
            #проверка на то, является ли пользователь автором поста (403, если нет)
            if post.owner == self.request.user:
                serializer = PostSerializer(post, data=data)
                #если нет ошибок - удаление старой картинки с сервера, обновление данных
                if serializer.is_valid():
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

    #удаление публикации
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            #проверка на то, является ли пользователь автором поста (403, если нет)
            if post.owner == self.request.user:
                #если прикреплена картинка, и она сохранена на сервере, то файл удаляется
                delete_image(post)
                post.delete()
                return Response({"message": "Публикация удалена"})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"message": "Публикация не найдена"},
                            status=status.HTTP_404_NOT_FOUND)