from django.urls import path

import comment.views

urlpatterns = [
    path("", comment.views.AllReviewView.as_view()),
    path("latest/", comment.views.ReviewLatestView.as_view()),
    path("random/", comment.views.ReviewRandomView.as_view()),
    path("hotest/", comment.views.ReviewRandomView.as_view()),
    path("<int:review_id>/", comment.views.ReviewView.as_view()),
    path("<int:review_id>/reply/", comment.views.ReviewReplyView.as_view()),
    path("<int:review_id>/like/", comment.views.ReviewLikeView.as_view())
]
