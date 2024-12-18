"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import AllPostView, PostAPI, CommentAPI, PostCreate, LikeAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_posts/', AllPostView.as_view()),
    path('post/<int:post_id>', PostAPI.as_view()),
    path('post/', PostCreate.as_view()),
    path('like/<int:post_id>', LikeAPI.as_view()),
    path('post/<int:post_id>/comment/', CommentAPI.as_view()),
    path('post/<int:post_id>/comment/<int:comment_id>', CommentAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)