import json
import math

from django.http import HttpResponse
from django.views import View
from celebrity.models import Celebrity, CelebrityImage
from movie.models import Movie, Position
from django.db.models import Q


class AllCelebrityView(View):
    def get(self, request):
        limit = request.GET.get("limit")
        page = request.GET.get("offset")

        if not all([limit, page]):
            return HttpResponse(content=json.dumps({"status": "缺少部分参数"}, ensure_ascii=False))

        try:
            limit = int(limit)
            page = int(page)
        except ValueError:
            return HttpResponse(content=json.dumps({"status": "参数类型错误"}, ensure_ascii=False))

        if limit <= 0 or page <= 0:
            return HttpResponse(content=json.dumps({"status": "参数错误"}, ensure_ascii=False))

        start = limit * (page - 1)
        total_item = Celebrity.objects.count()
        total_page = math.ceil(total_item / limit)

        if start > total_item:
            return HttpResponse(content=json.dumps({"status": "超出数据范围"}, ensure_ascii=False))

        end = min(start + limit, total_item)

        celebrities_info = Celebrity.objects.all()[start: end]
        celebrity_list = []

        for i in celebrities_info:
            celebrity_list.append(i.to_dict())

        meta = {"total_page": total_page, "total_item": total_item, "current_page": page}

        dic = {"meta": meta, "celebrities": celebrity_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class CelebrityView(View):
    def get(self, request, celebrity_id):
        celebrity = Celebrity.objects.filter(id=celebrity_id)

        if len(celebrity) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        dic = celebrity.get(id=celebrity_id).to_dict()

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class CelebritySearchView(View):
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
        total_item = Celebrity.objects.filter(celebrity_name__contains=query).count()
        total_page = math.ceil(total_item / limit)

        if start > total_item:
            return HttpResponse(content=json.dumps({"status": "超出数据范围"}, ensure_ascii=False))

        end = min(start + limit, total_item)

        celebrity_info = Celebrity.objects.filter(celebrity_name__contains=query)[start: end]
        celebrity_list = []

        for i in celebrity_info:
            celebrity_list.append(i.to_dict())

        meta = {"total_page": total_page, "total_item": total_item, "current_page": page}

        dic = {"meta": meta, "celebrities": celebrity_list}

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
                                               ~Q(id=celebrity_id)).distinct()

        celebrity_list = []
        for i in celebrities:
            celebrity_list.append(i.to_dict())

        dic = {"id": celebrity_id, "celebrities": celebrity_list}

        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))


class CelebrityMoviesView(View):
    def get(self, request, celebrity_id):
        if len(Celebrity.objects.filter(id=celebrity_id)) == 0:
            return HttpResponse(content=json.dumps({"status": "未找到影人"}, ensure_ascii=False))

        movies = Movie.objects.filter(position__celebrity_id=celebrity_id)
        movie_list = []
        for i in movies:
            movie_list.append(i.to_dict())

        dic = {"id": celebrity_id, "movies": movie_list}
        return HttpResponse(content=json.dumps(dic, ensure_ascii=False))

