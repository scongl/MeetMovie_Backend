from django.urls import path

import comment.views

urlpatterns = [
    path("", comment.views.AllReviewView.as_view()),
    path("<int:review_id>/", comment.views.ReviewView.as_view()),
    path("<int:review_id>/reply/", comment.views.ReviewReplyView.as_view()),
]
