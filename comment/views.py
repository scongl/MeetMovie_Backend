import json

from django.http import HttpResponse
from django.views import View
from comment.models import Review, Reply
from account.models import UserInfo

class AllReviewView(View):
    def get(self, request):
        reviews = Review.objects.all()
        review_list = []
        for review in reviews:
            author = review.author
            movie = review.movie

            d = review.to_dict()

            author_details = {"username": author.username, "nickname": author.nickname,
                              "id": author.id, "avatar": author.avatar.url}
            movie_details = {"movie_name": movie.movie_name, "movie_id": movie.id,
                             "movie_poster_path": movie.image}

            d["author_details"] = author_details
            d["movie_details"] = movie_details

            review_list.append(d)

        return HttpResponse(content=json.dumps(review_list, ensure_ascii=False))


class ReviewLatestView(View):
    def get(self, request):
        reviews = Review.objects.order_by("-create_at")[:min(1000, Review.objects.count())]
        movie_set = set({})

        review_list = []

        for review in reviews:
            if len(review_list) < 10 and review.movie.id not in movie_set:
                movie_set.add(review.movie.id)
                author = review.author
                movie = review.movie

                d = review.to_dict()

                author_details = author.to_dict()
                movie_details = movie.to_dict()

                d["author_details"] = author_details
                d["movie_details"] = movie_details

                review_list.append(d)

        return HttpResponse(content=json.dumps(review_list, ensure_ascii=False))


class ReviewRandomView(View):
    def get(self, request):
        reviews = Review.objects.order_by('?')[:min(10, Review.objects.count())]
        review_list = []

        for review in reviews:
            author = review.author
            movie = review.movie

            d = review.to_dict()

            author_details = author.to_dict()
            movie_details = movie.to_dict()

            d["author_details"] = author_details
            d["movie_details"] = movie_details

            review_list.append(d)

        return HttpResponse(content=json.dumps(review_list, ensure_ascii=False))


class ReviewView(View):
    def get(self, request, review_id):
        review_set = Review.objects.filter(id=review_id)
        if len(review_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = review_set.first()

        author = review.author
        movie = review.movie

        d = review.to_dict()

        author_details = {"username": author.username, "nickname": author.nickname,
                          "id": author.id, "avatar": author.avatar.url}

        movie_details = {"movie_name": movie.movie_name, "movie_id": movie.id,
                         "movie_poster_path": movie.image}

        d["author_details"] = author_details
        d["movie_details"] = movie_details

        return HttpResponse(content=json.dumps(d, ensure_ascii=False))

    def post(self, request, review_id):         # ????????????
        review_set = Review.objects.filter(id=review_id)
        if len(review_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = review_set.first()

        info = json.loads(request.body)
        title = info.get('title')
        content = info.get('content')

        if not all([title, content]):
            return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))

        if type(title) != str or type(content) != str:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        # TODO: ?????????????????????
        if not request.user.is_authenticated or review.author.id != request.user.id:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review.title = title
        review.content = content
        review.save()

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))

    def delete(self, request, review_id):
        review_set = Review.objects.filter(id=review_id)
        if len(review_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = review_set.first()

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        user: UserInfo = request.user
        if not (review.author.id == request.user.id or user.is_staff):
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review.delete()

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))


class ReviewLikeView(View):
    def post(self, request, review_id):
        if not Review.objects.filter(id=review_id).exists():
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = Review.objects.get(id=review_id)
        review.liked_user.add(request.user)

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))

    def delete(self, request, review_id):
        if not Review.objects.filter(id=review_id).exists():
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = Review.objects.get(id=review_id)
        review.liked_user.remove(request.user)

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))


class ReviewCurrentLikeView(View):
    def get(self, request, review_id):
        if not Review.objects.filter(id=review_id).exists():
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = Review.objects.get(id=review_id)
        if review.liked_user.filter(id=request.user.id).exists():
            return HttpResponse(content=json.dumps({"liked": True}, ensure_ascii=False))
        else:
            return HttpResponse(content=json.dumps({"liked": False}, ensure_ascii=False))


class ReviewReplyView(View):
    def get(self, request, review_id):
        review_set = Review.objects.filter(id=review_id)
        if len(review_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        replies = Reply.objects.filter(review_id=review_id)

        reply_list = []
        for reply in replies:
            author = reply.author

            d = reply.to_dict()

            author_details = {"username": author.username, "nickname": author.nickname,
                              "id": author.id, "avatar": author.avatar.url}

            d["author_details"] = author_details

            reply_list.append(d)

        dic = {"replies": reply_list, "reply_cnt": len(reply_list)}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

    def post(self, request, review_id):
        review_set = Review.objects.filter(id=review_id)
        if len(review_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        info = json.loads(request.body)
        content = info.get("content")

        if content is None:
            return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))

        if type(content) != str:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        review = review_set.first()
        Reply.objects.create(content=content, review=review, author=request.user)

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))


class ReplyView(View):
    def post(self, request, reply_id):              # ????????????
        reply_set = Reply.objects.filter(id=reply_id)
        if len(reply_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        info = json.loads(request.body)
        content = info.get("content")

        if content is None:
            return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))

        if type(content) != str:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        reply = reply_set.first()

        # TODO: ???????????????
        if not request.user.is_authenticated or reply.author.id != request.user.id:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        reply.content = content
        reply.save()

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))

    def delete(self, request, reply_id):
        reply_set = Reply.objects.filter(id=reply_id)
        if len(reply_set) == 0:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        reply = reply_set.first()

        if not request.user.is_authenticated:
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        user: UserInfo = request.user
        if not (reply.author.id == user.id or user.is_staff):
            return HttpResponse(content=json.dumps({"status": "???????????????"}, ensure_ascii=False))

        reply.delete()

        return HttpResponse(content=json.dumps({"status": "????????????"}, ensure_ascii=False))




