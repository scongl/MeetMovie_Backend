from django.urls import path

import group.views

urlpatterns = [
    path("", group.views.AllGroupView.as_view()),
    path("<int:group_id>/join/", group.views.GroupJoinView.as_view()),
    path("<int:group_id>/info/", group.views.GroupInfoView.as_view()),
    path("<int:group_id>/member/", group.views.GroupMemberView.as_view()),
    path("<int:group_id>/discussion/", group.views.GroupDiscussionView.as_view()),

]
