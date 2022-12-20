from django.contrib import admin
from .models import Movie, MovieImage, MovieTrailer, Genre
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    exclude = ('languages', )
    list_per_page = 20


class PageAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieImage, PageAdmin)
admin.site.register(MovieTrailer, PageAdmin)
admin.site.register(Genre, PageAdmin)

