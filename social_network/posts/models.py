from django.db import models
from django.contrib.auth.models import User

#from django.contrib.auth import get_user_model
#User = get_user_model()


class Post(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    text = models.TextField(blank = True)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                related_name='liked_post')
    #author = models.models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                related_name='commented_post')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
