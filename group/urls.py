from django.urls import path

import group.views

urlpatterns = [
    path("", group.views.AllGroupView.as_view()),

]
