from django.urls import path
import account.views

urlpatterns = [
    path("login/", account.views.LoginView.as_view(), name="login"),
    path("register/", account.views.RegisterView.as_view(), name="register"),
    path("logout/", account.views.LogoutView.as_view(), name="logout"),
    path("user/<int:user_id>/review/", account.views.UserReviewView.as_view()),
    path("user/<int:user_id>/info/", account.views.UserInfoView.as_view()),
    path("user/<int:user_id>/uploadavatar/", account.views.UploadAvatarView.as_view()),

]

