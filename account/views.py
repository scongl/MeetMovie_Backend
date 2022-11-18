import json

from django.http import HttpResponse
from django.contrib import auth
from django.views import View

from account.models import UserInfo
from comment.models import Review, Reply
from movie.models import Genre


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
                          "id": author.id, "avatar": author.avatar}
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





