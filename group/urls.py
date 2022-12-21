from django.urls import path

import group.views

urlpatterns = [
    path("", group.views.AllGroupView.as_view()),
    path("<int:group_id>/join/", group.views.GroupJoinView.as_view()),
    path("<int:group_id>/info/", group.views.GroupInfoView.as_view()),
    path("<int:group_id>/member/", group.views.GroupMemberView.as_view()),
    path("<int:group_id>/discussion/", group.views.GroupDiscussionView.as_view()),
    path("<int:group_id>/is_member/", group.views.GroupIsMemberView.as_view()),
    path("<int:group_id>/discussion/add/", group.views.GroupAddDiscussionView.as_view()),
    path("<int:group_id>/member/recent/", group.views.GroupRecentMember.as_view()),
    path("<int:group_id>/discussion/random/", group.views.GroupDiscussionRandomView.as_view()),
]
