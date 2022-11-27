from django.urls import path

import group.views

urlpatterns = [
    path("", group.views.AllGroupView.as_view()),
    path("<int:group_id>/join/", group.views.GroupJoinView.as_view()),

]
