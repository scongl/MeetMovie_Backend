import json

from django.views import View
from group.models import Group, Discussion, Comment, JoinTime
from django.http import HttpResponse
from account.models import UserInfo
import os


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

        if JoinTime.objects.filter(group_id=group_id, user=request.user).exists():
            return HttpResponse(content=json.dumps({"status": "用户已加入小组"}, ensure_ascii=False))

        group = Group.objects.get(id=group_id)
        JoinTime.objects.create(group=group, user=request.user)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))

    def delete(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        group = Group.objects.get(id=group_id)
        if JoinTime.objects.filter(group=group, user=request.user).exists():
            t = JoinTime.objects.get(group=group, user=request.user)
            t.delete()

        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))


class GroupCreateView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "无权限"}, ensure_ascii=False))
        if not request.user.is_staff:
            return HttpResponse(content=json.dumps({"status": "无权限"}, ensure_ascii=False))

        info = json.loads(request.body)
        name = info.get("name", "group")
        introduction = info.get("introduction", "")

        Group.objects.create(name=name, introduction=introduction)

        return HttpResponse(content=json.dumps({"status": "创建成功"}, ensure_ascii=False))


class GroupRemoveView(View):
    def delete(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "小组不存在"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "无权限"}, ensure_ascii=False))
        if not request.user.is_staff:
            return HttpResponse(content=json.dumps({"status": "无权限"}, ensure_ascii=False))

        Group.objects.get(id=group_id).delete()

        return HttpResponse(content=json.dumps({"status": "删除成功"}, ensure_ascii=False))


class UploadAvatar(View):
    def post(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "小组不存在"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "无权限"}, ensure_ascii=False))
        if not request.user.is_staff:
            return HttpResponse(content=json.dumps({"status": "无权限"}, ensure_ascii=False))

        avatar = request.FILES.get('avatar')
        if not avatar:
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        suffix = os.path.splitext(avatar.name)[1]
        if not suffix or suffix.lower() not in ['.jpeg', '.png', '.jpg', '.webp']:
            return HttpResponse(content=json.dumps({"status": "文件格式不对"}, ensure_ascii=False))

        g = Group.objects.get(id=group_id)
        g.avatar = avatar
        g.save()

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

        member_list = []

        for t in JoinTime.objects.filter(group_id=group_id):
            i = t.user
            member_list.append({"username": i.username, "nickname": i.nickname, "avatar": i.avatar.url,
                                "introduction": i.introduction, "id": i.id, "join_at": t.join_at.strftime("%Y-%m-%d")})

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
            dic["group"] = {"group_name": d.group.name, "id": d.group.id}
            discussion_list.append(dic)

        return HttpResponse(content=json.dumps(discussion_list, ensure_ascii=False))


class GroupAddDiscussionView(View):
    def post(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        if not JoinTime.objects.filter(group_id=group_id, user=request.user).exists():
            return HttpResponse(content=json.dumps({"status": "用户不属于本组"}, ensure_ascii=False))

        info = json.loads(request.body)
        title = info.get('title')
        content = info.get('content')

        if title is None or content is None:
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

    def delete(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        d = Discussion.objects.get(id=discussion_id)

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        user: UserInfo = request.user
        if not (user == d.author or user.is_staff):
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        d.delete()

        return HttpResponse(content=json.dumps({"status": "删除成功"}, ensure_ascii=False))


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


class CommentView(View):
    def delete(self, request, comment_id):
        if not Comment.objects.filter(id=comment_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到评论"}, ensure_ascii=False))

        c = Comment.objects.get(id=comment_id)
        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        user: UserInfo = request.user
        if not (user.id == c.author.id or user.is_staff):
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        c.delete()

        return HttpResponse(content=json.dumps({"status": "删除成功"}, ensure_ascii=False))


class DiscussionLikeView(View):
    def post(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        d = Discussion.objects.get(id=discussion_id)
        d.liked_user.add(request.user)

        return HttpResponse(content=json.dumps({"status": "更新成功"}, ensure_ascii=False))

    def delete(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        d = Discussion.objects.get(id=discussion_id)
        d.liked_user.remove(request.user)

        return HttpResponse(content=json.dumps({"status": "更新成功"}, ensure_ascii=False))


class DiscussionCurrentLikeView(View):
    def get(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        d = Discussion.objects.get(id=discussion_id)
        if d.liked_user.filter(id=request.user.id).exists():
            return HttpResponse(content=json.dumps({"liked": True}, ensure_ascii=False))
        else:
            return HttpResponse(content=json.dumps({"liked": False}, ensure_ascii=False))


class DiscussionAddCommentView(View):
    def post(self, request, discussion_id):
        if not Discussion.objects.filter(id=discussion_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到讨论"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        discussion = Discussion.objects.get(id=discussion_id)

        if not JoinTime.objects.filter(group_id=discussion.group.id, user=request.user).exists():
            return HttpResponse(content=json.dumps({"status": "用户不属于本组"}, ensure_ascii=False))

        info = json.loads(request.body)
        content = info.get('content')

        if content is None:
            return HttpResponse(content=json.dumps({"status": "缺少部分参数"}, ensure_ascii=False))

        Comment.objects.create(discussion_id=discussion_id, content=content, author_id=request.user.id)

        return HttpResponse(content=json.dumps({"status": "添加成功"}, ensure_ascii=False))


class GroupDiscussionRandomView(View):
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        max_count = Discussion.objects.filter(group_id=group_id).count()

        discussions = Discussion.objects.filter(group_id=group_id).order_by('?')[:min(5, max_count)]

        discussion_list = []
        for d in discussions:
            dic = d.to_dict()
            dic["group"] = {"group_name": d.group.name, "id": group_id}
            dic["author"] = d.author.to_dict()
            discussion_list.append(dic)

        return HttpResponse(content=json.dumps(discussion_list, ensure_ascii=False))


class GroupRecentMember(View):
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse(content=json.dumps({"status": "未找到小组"}, ensure_ascii=False))

        total_count = JoinTime.objects.filter(group_id=group_id).count()

        join_times = JoinTime.objects.filter(group_id=group_id).order_by('-join_at')[:min(5, total_count)]

        member_list = []
        for i in join_times:
            dic = i.user.to_dict()
            dic["join_at"] = i.join_at.strftime("%Y-%m-%d")
            member_list.append(dic)

        return HttpResponse(content=json.dumps(member_list, ensure_ascii=False))









