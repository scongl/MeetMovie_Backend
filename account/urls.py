from django.urls import path
import account.views

urlpatterns = [
    path("login/", account.views.LoginView.as_view()),
    path("register/", account.views.RegisterView.as_view()),
    path("logout/", account.views.LogoutView.as_view()),
    path("user/<int:user_id>/review/", account.views.UserReviewView.as_view()),
    path("user/<int:user_id>/info/", account.views.UserInfoView.as_view()),
    path("user/<int:user_id>/uploadavatar/", account.views.UploadAvatarView.as_view()),
    path("user/<int:user_id>/starmovies/", account.views.UserMovieView.as_view()),
    path("user/<int:user_id>/starcelebrities/", account.views.UserCelebrityView.as_view()),
    path("user/<int:user_id>/starmovie/<int:movie_id>/", account.views.UserStarMovieView.as_view()),
    path("user/<int:user_id>/starcelebrity/<int:celebrity_id>/", account.views.UserStarCelebrityView.as_view()),
    path("user/<int:user_id>/groups/", account.views.UserGroupView.as_view()),
    path("user/<int:user_id>/updateinfo/", account.views.UserUpdateView.as_view())
]

