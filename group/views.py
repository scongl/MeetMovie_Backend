import json

from django.views import View
from group.models import Group, Discussion, Comment
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
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        group = Group.objects.get(id=group_id)
        group.members.add(request.user)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))

    def delete(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        group = Group.objects.get(id=group_id)
        # 用户未加入过小组不会有影响
        group.members.remove(request.user)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))


class GroupInfoView(View):
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        t = Group.objects.get(id=group_id)

        return HttpResponse(content=json.dumps(t.to_dict(), ensure_ascii=False))


class GroupMemberView(View):
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        t = Group.objects.get(id=group_id)

        member_list = []

        for i in t.members.all():
            member_list.append({"username": i.username, "nickname": i.nickname, "avatar": i.avatar.url, "id": i.id})

        t = {"group_members": member_list}

        return HttpResponse(content=json.dumps(t, ensure_ascii=False))


class GroupDiscussionView(View):
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        discussions = Discussion.objects.filter(group=group_id)

        discussion_list = []

        for discuss in discussions:
            dic = discuss.to_dict()
            author = discuss.author
            dic["author"] = {"username": author.username, "nickname": author.nickname,
                             "avatar": author.avatar.url, "id": author.id}

            discussion_list.append(dic)

        return HttpResponse(content=json.dumps({"discussions": discussion_list}, ensure_ascii=False))


class GroupIsMemberView(View):
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"is_member": False}, ensure_ascii=False))

        g = Group.objects.get(id=group_id)

        if not g.members.filter(id=request.user.id).exists():
            return HttpResponse(content=json.dumps({"is_member": False}, ensure_ascii=False))
        else:
            return HttpResponse(content=json.dumps({"is_member": True}, ensure_ascii=False))


class DiscussionRandomView(View):
    def get(self, request):
        discussions = Discussion.objects.order_by('?')[:min(5, Discussion.objects.count())]

        discussion_list = []
        for d in discussions:
            dic = d.to_dict()
            dic["group_name"] = d.group.name
            discussion_list.append(dic)

        return HttpResponse(content=json.dumps(discussion_list, ensure_ascii=False))


class GroupAddDiscussionView(View):
    def post(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        info = json.loads(request.body)
        title = info.get('title')
        content = info.get('content')

        if not all([title, content]):
            return HttpResponse(content=json.dumps({"status": "缺少部分参数"}, ensure_ascii=False))

        Discussion.objects.create(group_id=group_id, author_id=request.user.id, title=title, content=content)

        return HttpResponse(content=json.dumps({"status": "添加成功"}, ensure_ascii=False))


class DiscussionView(View):
    def get(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        d = Discussion.objects.get(id=discussion_id)

        dic = d.to_dict()
        author = d.author
        dic["author"] = {"username": author.username, "nickname": author.nickname,
                         "id": author.id, "avatar": author.avatar.url}

        group = d.group
        group_info = group.to_dict()
        group_info["member_count"] = group.members.count()
        dic["group"] = group_info
        dic["reply_count"] = d.comment_set.count()

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class DiscussionCommentView(View):
    def get(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        comments = Comment.objects.filter(discussion_id=discussion_id)
        comment_list = []

        for i in comments:
            dic = i.to_dict()
            author = i.author
            dic["author"] = author.to_dict()
            comment_list.append(dic)

        return HttpResponse(content=json.dumps(comment_list, ensure_ascii=False))


class DiscussionLikeView(View):
    def post(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        d = Discussion.objects.get(id=discussion_id)
        d.likes = d.likes + 1
        d.save()

        return HttpResponse(content=json.dumps({"status": "更新成功"}, ensure_ascii=False))


class DiscussionAddCommentView(View):
    def post(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        info = json.loads(request.body)
        content = info.get('content')

        if not content:
            return HttpResponse(content=json.dumps({"status": "缺少部分参数"}, ensure_ascii=False))

        Comment.objects.create(discussion_id=discussion_id, content=content, author_id=request.user.id)

        return HttpResponse(content=json.dumps({"status": "添加成功"}, ensure_ascii=False))













