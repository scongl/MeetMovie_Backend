import json

from django.http import HttpResponse
from django.views import View
from celebrity.models import Celebrity, CelebrityImage
from movie.models import Movie, Position
from django.db.models import Q


class AllCelebrityView(View):
    def get(self, request):
        celebrities_info = Celebrity.objects.values()
        celebrity_list = []

        for i in celebrities_info:
            celebrity_list.append(i)
        return HttpResponse(content=json.dumps(celebrity_list, ensure_ascii=False))


class CelebrityView(View):
    def get(self, request, celebrity_id):
        celebrity = Celebrity.objects.filter(id=celebrity_id)

        if len(celebrity) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        dic = celebrity.values().get(id=celebrity_id)

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class CelebrityImagesView(View):
    def get(self, request, celebrity_id):
        if len(Celebrity.objects.filter(id=celebrity_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        all_photos = CelebrityImage.objects.filter(celebrity_id=celebrity_id)
        dic = {"id": celebrity_id}
        images = []
        for photo in all_photos:
            images.append({"image_path": photo.path})
        dic["images"] = images

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class CelebrityCooperateView(View):
    def get(self, request, celebrity_id):
        if len(Celebrity.objects.filter(id=celebrity_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        movie_ids = Position.objects.filter(celebrity_id=celebrity_id).distinct().values("movie_id")
        movie_list = []
        for i in movie_ids:
            movie_list.append(i.get("movie_id"))

        celebrities = Celebrity.objects.filter(Q(position__movie_id__in=movie_list),
                                               ~Q(id=celebrity_id)).distinct().values()

        celebrity_list = []
        for i in celebrities:
            celebrity_list.append(i)

        dic = {"id": celebrity_id, "celebrities": celebrity_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class CelebrityMoviesView(View):
    def get(self, request, celebrity_id):
        if len(Celebrity.objects.filter(id=celebrity_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        movies = Movie.objects.filter(position__celebrity_id=celebrity_id).values()
        movie_list = []
        for i in movies:
            i['vote_average'] = i["vote_sum"] / i["vote_count"] if i["vote_count"] > 0 else 0.0
            movie_list.append(i)

        dic = {"id": celebrity_id, "movies": movie_list}
        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

