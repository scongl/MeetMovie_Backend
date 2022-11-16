import json

from django.http import HttpResponse
from django.views import View
from movie.models import Movie, Position, Genre, MovieImage, MovieTrailer
from celebrity.models import Celebrity
from comment.models import Review, Rating, Reply
from account.models import UserInfo


class AllMovieView(View):
    def get(self, request):
        movies_info = Movie.objects.values()
        movie_list = []
        for i in movies_info:
            i['vote_average'] = i["vote_sum"] / i["vote_count"] if i["vote_count"] > 0 else 0.0

            genres = Genre.objects.filter(movie=i.get("id")).distinct().values()
            genre_list = []
            for j in genres:
                genre_list.append(j)

            i["genres"] = genre_list
            movie_list.append(i)

        return HttpResponse(content=json.dumps(movie_list, ensure_ascii=False))


class MovieView(View):
    def get(self, request, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        dic = Movie.objects.values().get(id=movie_id)

        genres = Genre.objects.filter(movie=movie_id).distinct().values()
        genre_list = []

        for i in genres:
            genre_list.append(i)

        dic["genres"] = genre_list
        dic["vote_average"] = dic["vote_sum"] / dic["vote_count"] if dic["vote_count"] > 0 else 0.0

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieImageView(View):
    def get(self, request, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        all_photos = MovieImage.objects.filter(movie_id=movie_id)
        dic = {"id": movie_id}
        images = []
        for photo in all_photos:
            images.append({"image_path": photo.path})
        dic["images"] = images

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieVideoView(View):
    def get(self, request, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        video = MovieTrailer.objects.filter(movie_id=movie_id).first()
        dic = {"id": movie_id}
        videos = [{"video_path": video.path if video else None}]
        dic["videos"] = videos

        return HttpResponse(json.dumps(dic, ensure_ascii=False))


class MovieCelebritiesView(View):
    def get(self, request, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        celebrity_info = Celebrity.objects.filter(position__movie_id=movie_id).distinct().values()
        celebrity_list = []

        for i in celebrity_info:
            celebrity_list.append(i)

        dic = {"id": movie_id, "celebrities": celebrity_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieReviewView(View):
    def get(self, request, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        reviews = Review.objects.filter(movie_id=movie_id).distinct().values()

        review_list = []

        for i in reviews:
            user = UserInfo.objects.get(comment=i.get("id"))

            i["author_details"] = {"username": user.username, "nickname": user.nickname,
                                   "id": user.id, "avatar": user.avatar}

            # 将datetime类转换为字符串
            i["update_at"] = i["update_at"].strftime("%Y-%m-%d %H:%M:%S")
            i["create_at"] = i["create_at"].strftime("%Y-%m-%d %H:%M:%S")

            replies = Reply.objects.filter(review_id=i.get("id"))
            reply_list = []
            for j in replies:
                t = {"content": j.content, "create_at": j.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                     "update_at": j.update_at.strftime("%Y-%m-%d %H:%M:%S")}
                author = j.author
                t["author_details"] = {"username": author.username, "nickname": author.nickname,
                                       "id": author.id, "avatar": author.avatar}
                reply_list.append(t)

            i["replies"] = reply_list

            review_list.append(i)

        dic = {"reviews": review_list, "id": movie_id}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

    def post(self, request, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        info = json.loads(request.body)
        title = info.get('title')
        content = info.get('content')

        if not all([title, content]):
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        if type(title) != str or type(content) != str:
            return HttpResponse(content=json.dumps({"status": "参数不正确"}, ensure_ascii=False))

        Review.objects.create(title=title, content=content, author=request.user, movie_id=movie_id)

        return HttpResponse(content=json.dumps({"status": "提交成功"}, ensure_ascii=False))


class MovieRatingView(View):
    def movie_valid(self, movie_id):
        if len(Movie.objects.filter(id=movie_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到电影"}, ensure_ascii=False))

    def get(self, request, movie_id):
        self.movie_valid(movie_id)

        ratings = Rating.objects.filter(movie_id=movie_id)
        rating_list = []
        dic = {}

        if request.user.is_authenticated:  # 当前用户已登录
            # 若当前用户未评分过，current_user值为null
            t = None
            for i in ratings:
                author = i.author
                info = {"value": i.value,
                        "content": i.content,
                        "author_details": {"username": author.username,
                                           "nickname": author.nickname,
                                           "avatar": author.avatar,
                                           "id": author.id
                                           }
                        }
                if i.author == request.user:
                    t = info

                rating_list.append(info)

            dic["rating"] = rating_list
            dic["current_user"] = t
        else:
            for i in ratings:
                author = i.author
                info = {"value": i.value,
                        "content": i.content,
                        "author_details": {"username": author.username,
                                           "nickname": author.nickname,
                                           "avatar": author.avatar,
                                           "id": author.id
                                           }
                        }
                rating_list.append(info)
            dic["rating"] = rating_list
            dic["current_user"] = None

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

    def post(self, request, movie_id):
        self.movie_valid(movie_id)

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        info = json.loads(request.body)
        value = info.get("value")
        content = info.get("content")

        if not all([value, content]):
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        if value not in range(1, 11) or type(content) != str:
            return HttpResponse(content=json.dumps({"status": "参数不正确"}, ensure_ascii=False))

        user_id = request.user.id

        r = Rating.objects.filter(movie_id=movie_id, author_id=user_id)
        if len(r) == 0:  # 未提交过评分
            Rating.objects.create(author_id=user_id, movie_id=movie_id, value=value, content=content)

            movie = Movie.objects.get(id=movie_id)

            movie.vote_count += 1
            movie.vote_sum += value

            movie.save()

            return HttpResponse(content=json.dumps({"status": "提交成功"}, ensure_ascii=False))

        else:  # 修改评分和评论
            rating = r.first()
            old_value = rating.value
            rating.value = value
            rating.content = content

            movie = Movie.objects.get(id=movie_id)
            movie.vote_sum += value - old_value

            movie.save()
            return HttpResponse(content=json.dumps({"status": "提交成功"}, ensure_ascii=False))

    def delete(self, request, movie_id):
        self.movie_valid(movie_id)

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        user_id = request.user.id

        if len(Rating.objects.filter(movie_id=movie_id, author_id=user_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "用户未提交过评分"}, ensure_ascii=False))

        rating = Rating.objects.get(movie_id=movie_id, author_id=user_id)
        value = rating.value
        rating.delete()

        movie = Movie.objects.get(id=movie_id)

        movie.vote_count -= 1
        movie.vote_sum -= value

        movie.save()

        return HttpResponse(content=json.dumps({"status": "删除评分成功"}, ensure_ascii=False))
