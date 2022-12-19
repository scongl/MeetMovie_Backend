import json
import os.path

from django.http import HttpResponse
from django.contrib import auth
from django.views import View

from account.models import UserInfo
from comment.models import Review, Reply
from movie.models import Movie, Genre
from celebrity.models import Celebrity
from group.models import Group


class LoginView(View):
    def get(self, request):
        return HttpResponse()

    def post(self, request):
        info = json.loads(request.body)

        username = info.get("username")
        password = info.get("password")

        if not all([username, password]):
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        if type(username) != str or type(password) != str:
            return HttpResponse(content=json.dumps({"status": "参数类型不正确"}, ensure_ascii=False))

        # 查询是否有对应用户
        user = auth.authenticate(username=username, password=password)

        if user:
            # 此处会创建session, 并返回sessionId
            auth.login(request, user)
            return HttpResponse(content=json.dumps({"string": "登录成功"}, ensure_ascii=False))
        else:
            # 不存在对应用户
            return HttpResponse(content=json.dumps({"error": "用户名或密码错误"}, ensure_ascii=False))


class LogoutView(View):
    def get(self, request):
        # 用户未登录
        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"error": "未登录"}, ensure_ascii=False))

        auth.logout(request)
        return HttpResponse(content=json.dumps({"string": "退出成功"}, ensure_ascii=False))


class RegisterView(View):
    def get(self, request):
        return HttpResponse()

    def post(self, request):
        info = json.loads(request.body)

        username = info.get("username")
        password = info.get("password")

        if not all([username, password]):
            return HttpResponse(content=json.dumps({"error": "缺少参数"}, ensure_ascii=False))

        if type(username) != str or type(password) != str:
            return HttpResponse(content=json.dumps({"status": "参数类型不正确"}, ensure_ascii=False))

        # 用户已存在
        if UserInfo.objects.filter(username=username):
            return HttpResponse(content=json.dumps({"error": "用户名已存在"}, ensure_ascii=False))

        else:
            UserInfo.objects.create_user(username=username, password=password, nickname=username)
            return HttpResponse(content=json.dumps({"string": "注册成功"}, ensure_ascii=False))


class UserReviewView(View):
    def get(self, request, user_id):
        user_set = UserInfo.objects.filter(id=user_id)
        if len(user_set) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        reviews = Review.objects.filter(author_id=user_id)

        author = user_set.first()

        author_details = {"username": author.username, "nickname": author.nickname,
                          "id": author.id, "avatar": author.avatar.url}
        review_list = []
        for review in reviews:
            d = {"id": review.id, "title": review.title, "content": review.content,
                 "create_at": review.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                 "update_at": review.update_at.strftime("%Y-%m-%d %H:%M:%S")}

            movie = review.movie
            movie_details = {"movie_name": movie.movie_name, "movie_id": movie.id,
                             "movie_poster_path": movie.image}

            d["author_details"] = author_details
            d["movie_details"] = movie_details

            review_list.append(d)

        return HttpResponse(content=json.dumps(review_list, ensure_ascii=False))


class UserInfoView(View):
    def get(self, request, user_id):
        user_set = UserInfo.objects.filter(id=user_id)
        if len(user_set) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        user = user_set.first()

        d = user.to_dict()

        genres = Genre.objects.filter(userinfo=user).distinct().values()
        genre_list = []
        for j in genres:
            genre_list.append(j)

        d["prefer_types"] = genre_list

        return HttpResponse(content=json.dumps(d, ensure_ascii=False))


class UploadAvatarView(View):
    def post(self, request, user_id):
        # 图片通过表单发送
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        avatar = request.FILES.get('avatar')
        if not avatar:
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        suffix = os.path.splitext(avatar.name)[1]
        if not suffix or suffix.lower() not in ['.jpeg', '.png', '.jpg', '.webp']:
            return HttpResponse(content=json.dumps({"status": "文件格式不对"}, ensure_ascii=False))

        # TODO: 目前修改头像后不会将原先无用的图片删除掉
        user = UserInfo.objects.get(id=user_id)
        user.avatar = avatar
        user.save()

        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))


class UserMovieView(View):
    def get(self, request, user_id):
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        user = UserInfo.objects.get(id=user_id)
        movie_list = []
        for movie in user.like_movies.all():
            d = movie.to_dict()
            movie_list.append(d)

        return HttpResponse(content=json.dumps(movie_list, ensure_ascii=False))


class UserCelebrityView(View):
    def get(self, request, user_id):
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        user = UserInfo.objects.get(id=user_id)
        celebrity_list = []
        for celebrity in user.like_celebrities.all():
            d = celebrity.to_dict()
            celebrity_list.append(d)

        return HttpResponse(content=json.dumps(celebrity_list, ensure_ascii=False))


class UserStarMovieView(View):
    def post(self, request, user_id, movie_id):
        # 用户必须登录且只能修改自己的
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))
        if Movie.objects.filter(id=movie_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        if request.user.id != user_id:
            # TODO: 管理员也可修改
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        # 若已添加则无影响
        request.user.like_movies.add(movie_id)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))

    def delete(self, request, user_id, movie_id):
        # 用户必须登录且只能修改自己的
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))
        if Movie.objects.filter(id=movie_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        if request.user.id != user_id:
            # TODO: 管理员也可修改
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        request.user.like_movies.remove(movie_id)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))


class UserStarCelebrityView(View):
    def post(self, request, user_id, celebrity_id):
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))
        if Celebrity.objects.filter(id=celebrity_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        if request.user.id != user_id:
            # TODO: 管理员也可修改
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        # 若已添加则无影响
        request.user.like_celebrities.add(celebrity_id)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))

    def delete(self, request, user_id, celebrity_id):
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))
        if Celebrity.objects.filter(id=celebrity_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        if request.user.id != user_id:
            # TODO: 管理员也可修改
            return HttpResponse(content=json.dumps({"status": "无删除权限"}, ensure_ascii=False))

        request.user.like_celebrities.remove(celebrity_id)
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))


class UserGroupView(View):
    def get(self, request, user_id):
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        groups = Group.objects.filter(members=user_id)
        group_list = []
        for group in groups:
            group_list.append(group.to_dict())

        return HttpResponse(content=json.dumps(group_list, ensure_ascii=False))


class UserUpdateView(View):
    def post(self, request, user_id):
        if UserInfo.objects.filter(id=user_id).count() == 0:
            return HttpResponse(content=json.dumps({"status": "未找到用户"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        if request.user.id != user_id:
            return HttpResponse(content=json.dumps({"status": "无修改权限"}, ensure_ascii=False))

        user: UserInfo = request.user

        info = json.loads(request.body)
        username = info.get('username')
        nickname = info.get('nickname')
        introduction = info.get('introduction')
        prefer_types = info.get('prefer_types')
        email = info.get('email')

        if not all([username, nickname, introduction, prefer_types, email]):
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        user.username = username
        user.nickname = nickname
        user.introduction = introduction
        user.email = email
        user.prefer_genres.clear()
        for i in prefer_types:
            g = Genre.objects.filter(name=i)
            if len(g) == 0:
                continue
            genre = g.first()
            user.prefer_genres.add(genre)

        user.save()
        return HttpResponse(content=json.dumps({"status": "修改成功"}, ensure_ascii=False))



