import json
import math
import re

from django.db.models import Q, F
from django.http import HttpResponse
from django.views import View
from movie.models import Movie, Position, Genre, MovieImage, MovieTrailer
from celebrity.models import Celebrity
from comment.models import Review, Rating, Reply
from account.models import UserInfo


class AllMovieView(View):
    # def get(self, request):
    #     movies_info = Movie.objects.values()
    #     movie_list = []
    #     for i in movies_info:
    #         i['vote_average'] = i["vote_sum"] / i["vote_count"] if i["vote_count"] > 0 else 0.0
    #
    #         genres = Genre.objects.filter(movie=i.get("id")).distinct().values()
    #         genre_list = []
    #         for j in genres:
    #             genre_list.append(j)
    #
    #         i["genres"] = genre_list
    #         movie_list.append(i)
    #
    #     return HttpResponse(content=json.dumps(movie_list, ensure_ascii=False))

    def release_date_filter(self, filter_data: dict):
        release_date_gap = filter_data.get('release_date_gap')
        if release_date_gap is None:
            return []

        from_date = release_date_gap[0]
        end_date = release_date_gap[1]

        return [Q(release_date__gte=from_date), Q(release_date__lte=end_date)]

    def genres_filter(self, filter_data: dict):
        genres = filter_data.get('genres')
        if genres is None:
            return []
        genre_id_list = [i.get('id') for i in genres]

        return [Q(genres__in=genre_id_list)]

    def language_filter(self, filter_data: dict):
        language = filter_data.get('language')
        if language is None:
            return []

        return [Q(languages__name__in=language)]

    def rating_filter(self, filter_data: dict):
        min_rating = filter_data.get('min_rating')
        if min_rating is None:
            return []

        return [Q(vote_sum__gte=F('vote_count') * min_rating)]

    def duration_filter(self, filter_data: dict):
        duration_gap = filter_data.get('duration_gap')
        if duration_gap is None:
            return []

        min_value = duration_gap[0]
        max_value = duration_gap[1]

        return [Q(duration__gte=min_value), Q(duration__lte=max_value)]

    def post(self, request):
        info = json.loads(request.body)
        limit = info.get('limit')
        page = info.get('offset')

        range_at = info.get('range_at')
        filter_data = info.get('filter')

        if not all([limit, page]):
            return HttpResponse(content=json.dumps({"status": "缺少部分参数"}, ensure_ascii=False))

        if type(limit) != int or type(page) != int or limit <= 0 or page <= 0:
            return HttpResponse(content=json.dumps({"status": "参数错误"}, ensure_ascii=False))

        filter_list = self.genres_filter(filter_data) + self.rating_filter(filter_data) + \
                      self.duration_filter(filter_data) + self.release_date_filter(filter_data) + \
                      self.language_filter(filter_data)

        satisfied_movie = Movie.objects.filter(*filter_list)
        start = limit * (page - 1)
        total_item = satisfied_movie.count()
        total_page = math.ceil(total_item / limit)

        if start > total_item:
            return HttpResponse(content=json.dumps({"status": "超出数据范围"}, ensure_ascii=False))

        end = min(start + limit, total_item)

        if range_at == 0:
            movie_info = Movie.objects.filter(*filter_list)[start: end]
        elif range_at == 1:
            movie_info = Movie.objects.filter(*filter_list).order_by("-release_date")[start: end]
        else:
            movie_info = Movie.objects.filter(*filter_list). \
                             order_by((F('vote_sum') / F('vote_count')).desc())[start: end]

        movie_list = []
        for i in movie_info:
            t = i.to_dict()
            genres = Genre.objects.filter(movie=i.id).distinct().values()
            genre_list = []
            for j in genres:
                genre_list.append(j)

            t["genres"] = genre_list
            movie_list.append(t)

        meta = {"total_page": total_page, "total_item": total_item, "current_page": page}

        dic = {"meta": meta, "movies": movie_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieSearchView(View):
    def get(self, request):
        limit = request.GET.get("limit")
        page = request.GET.get("offset")
        query = request.GET.get("query")

        if not all([limit, page, query]):
            return HttpResponse(content=json.dumps({"status": "缺少部分参数"}, ensure_ascii=False))

        try:
            limit = int(limit)
            page = int(page)
        except ValueError:
            return HttpResponse(content=json.dumps({"status": "参数类型错误"}, ensure_ascii=False))

        if limit <= 0 or page <= 0:
            return HttpResponse(content=json.dumps({"status": "参数错误"}, ensure_ascii=False))

        start = limit * (page - 1)
        total_item = Movie.objects.filter(movie_name__contains=query).count()
        total_page = math.ceil(total_item / limit)

        if start > total_item:
            return HttpResponse(content=json.dumps({"status": "超出数据范围"}, ensure_ascii=False))

        end = min(start + limit, total_item)

        movie_info = Movie.objects.filter(movie_name__contains=query)[start: end]
        movie_list = []

        for i in movie_info:
            movie_list.append(i.to_dict())

        meta = {"total_page": total_page, "total_item": total_item, "current_page": page}

        dic = {"meta": meta, "movies": movie_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        dic = Movie.objects.get(id=movie_id).to_dict()

        genres = Genre.objects.filter(movie=movie_id).distinct()
        genre_list = []

        for i in genres:
            genre_list.append(i.to_dict())

        dic["genres"] = genre_list

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieImageView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        all_photos = MovieImage.objects.filter(movie_id=movie_id)
        dic = {"id": movie_id}
        images = []
        for photo in all_photos:
            images.append({"image_path": photo.path})
        dic["images"] = images

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieVideoView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        video = MovieTrailer.objects.filter(movie_id=movie_id).first()
        dic = {"id": movie_id}
        videos = [{"video_path": video.path if video else None}]
        dic["videos"] = videos

        return HttpResponse(json.dumps(dic, ensure_ascii=False))


class MovieCelebritiesView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        celebrity_info = Celebrity.objects.filter(position__movie_id=movie_id).distinct()
        celebrity_list = []

        for i in celebrity_info:
            celebrity_list.append(i.to_dict())

        dic = {"id": movie_id, "celebrities": celebrity_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieStaffView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        position = request.GET.get('position')

        if not position:
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        try:
            position = int(position)
        except ValueError:
            return HttpResponse(content=json.dumps({"status": "参数类型错误"}, ensure_ascii=False))

        if position not in [0, 1, 2]:
            return HttpResponse(content=json.dumps({"status": "参数错误"}, ensure_ascii=False))

        staff_set = Celebrity.objects.filter(position__movie_id=movie_id, position__position=position)
        staff_list = []

        for i in staff_set:
            staff_list.append(i.to_dict())

        dic = {"id": movie_id, "staffs": staff_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class MovieReviewView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        reviews = Review.objects.filter(movie_id=movie_id).distinct()

        review_list = []

        for i in reviews:
            review_dic = i.to_dict()

            author = i.author
            review_dic["author_details"] = {"username": author.username, "nickname": author.nickname,
                                            "id": author.id, "avatar": author.avatar.url}

            replies = Reply.objects.filter(review_id=i.id)
            reply_list = []
            for j in replies:
                reply_dic = j.to_dict()
                author = j.author
                reply_dic["author_details"] = {"username": author.username, "nickname": author.nickname,
                                               "id": author.id, "avatar": author.avatar.url}
                reply_list.append(reply_dic)

            review_dic["replies"] = reply_list
            review_dic["reply_cnt"] = len(reply_list)

            review_list.append(review_dic)

        dic = {"reviews": review_list, "id": movie_id}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

    def post(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

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
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        ratings = Rating.objects.filter(movie_id=movie_id)
        rating_list = []
        dic = {}

        if request.user.is_authenticated:  # 当前用户已登录
            # 若当前用户未评分过，current_user值为null
            t = None
            for i in ratings:
                author = i.author

                info = i.to_dict()

                info["author_details"] = {"username": author.username, "nickname": author.nickname,
                                          "avatar": author.avatar.url, "id": author.id}

                if i.author == request.user:
                    t = info

                rating_list.append(info)

            dic["rating"] = rating_list
            dic["current_user"] = t
        else:
            for i in ratings:
                author = i.author
                info = i.to_dict()
                info["author_details"] = {"username": author.username, "nickname": author.nickname,
                                          "avatar": author.avatar.url, "id": author.id}
                rating_list.append(info)

            dic["rating"] = rating_list
            dic["current_user"] = None

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

    def post(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        info = json.loads(request.body)
        value = info.get("value")
        content = info.get("content")

        if not all([value, content]):
            return HttpResponse(content=json.dumps({"status": "缺少参数"}, ensure_ascii=False))

        if value not in range(0, 11) or type(content) != str:
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
            rating.save()

            movie = Movie.objects.get(id=movie_id)
            movie.vote_sum += value - old_value

            movie.save()
            return HttpResponse(content=json.dumps({"status": "提交成功"}, ensure_ascii=False))

    def delete(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

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


class GenreView(View):
    def get(self, request):
        genres = Genre.objects.all()
        genre_list = []
        for i in genres:
            genre_list.append(i.to_dict())

        return HttpResponse(content=json.dumps({"genres": genre_list}, ensure_ascii=False))


class MovieCurrentLikeView(View):
    def get(self, request, movie_id):
        if not Movie.objects.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"status": "电影不存在"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "用户未登录"}, ensure_ascii=False))

        user: UserInfo = request.user
        if user.like_movies.filter(id=movie_id).exists():
            return HttpResponse(content=json.dumps({"liked": True}, ensure_ascii=False))
        else:
            return HttpResponse(content=json.dumps({"liked": False}, ensure_ascii=False))
