from django.db import models
from django.contrib.auth.models import User


#Публикации
class Post(models.Model):
    text = models.TextField(blank = True)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

#Лайки - каждый от определённого пользователя к конкретной публикации
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                related_name='liked_post')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

#Комментарии к публикациям
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                related_name='commented_post')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
