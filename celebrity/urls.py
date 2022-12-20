from django.urls import path
import celebrity.views

urlpatterns = [
    path("", celebrity.views.AllCelebrityView.as_view()),
    path("<int:celebrity_id>/", celebrity.views.CelebrityView.as_view()),
    path("<int:celebrity_id>/celebrities/", celebrity.views.CelebrityCooperateView.as_view()),
    path("<int:celebrity_id>/movies/", celebrity.views.CelebrityMoviesView.as_view()),
    path("<int:celebrity_id>/images/", celebrity.views.CelebrityImagesView.as_view()),
    path("<int:celebrity_id>/current_like/", celebrity.views.CelebrityCurrentLikeView.as_view())
]
