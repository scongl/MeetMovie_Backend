from django.urls import path
import movie.views

urlpatterns = [
    path("", movie.views.AllMovieView.as_view()),
    path("<int:movie_id>/", movie.views.MovieView.as_view()),
    path("<int:movie_id>/images", movie.views.MovieImageView.as_view()),
    path("<int:movie_id>/celebrities/", movie.views.MovieCelebritiesView.as_view()),
    path("<int:movie_id>/staffs/", movie.views.MovieStaffView.as_view()),
    path("<int:movie_id>/review/", movie.views.MovieReviewView.as_view()),
    path("<int:movie_id>/rating/", movie.views.MovieRatingView.as_view()),
    path("<int:movie_id>/images/", movie.views.MovieImageView.as_view()),
    path("<int:movie_id>/videos/", movie.views.MovieVideoView.as_view()),
    path("<int:movie_id>/current_like/", movie.views.MovieCurrentLikeView.as_view())
]

