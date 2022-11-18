import json

from django.shortcuts import render
from django.views import View
from group.models import Group
from django.http import HttpResponse


class AllGroupView(View):
    def get(self, request):
        group_set = Group.objects.all()
        group_list = []
        for i in group_set:
            group_list.append(i.to_dict())

        dic = {"groups": group_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class GroupJoinView(View):
    def post(self, request, group_id):
        if Group.objects.filter(id=group_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        group = Group.objects.get(group_id)
        group.members.filter()








