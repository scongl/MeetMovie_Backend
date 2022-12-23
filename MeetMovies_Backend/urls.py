"""MeetMovies_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from comment.views import ReplyView
from movie.views import MovieSearchView, GenreView
from celebrity.views import CelebritySearchView
from group.views import DiscussionRandomView, DiscussionView, DiscussionCommentView, DiscussionLikeView, \
    DiscussionAddCommentView, DiscussionCurrentLikeView, CommentView


import account.urls
import account.views
import celebrity.urls
import comment.urls
import movie.urls
import group.urls

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include(account.urls)),

    path("celebrity/", include(celebrity.urls)),
    path("movie/", include(movie.urls)),
    path("review/", include(comment.urls)),
    path("group/", include(group.urls)),

    path("reply/<int:reply_id>/", ReplyView.as_view()),
    path("search/movie/", MovieSearchView.as_view()),
    path("search/celebrity/", CelebritySearchView.as_view()),
    path("genre/", GenreView.as_view()),
    path("discussion/random/", DiscussionRandomView.as_view()),
    path("discussion/<int:discussion_id>/", DiscussionView.as_view()),
    path("discussion/<int:discussion_id>/comment/", DiscussionCommentView.as_view()),
    path("discussion/<int:discussion_id>/like/", DiscussionLikeView.as_view()),
    path("discussion/<int:discussion_id>/comment/add/", DiscussionAddCommentView.as_view()),
    path("discussion/<int:discussion_id>/current_like/", DiscussionCurrentLikeView.as_view()),
    path("comment/<int:comment_id>/", CommentView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


