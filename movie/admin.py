from django.contrib import admin
from .models import Movie, MovieImage, MovieTrailer, Genre
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    exclude = ('languages', )


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieImage)
admin.site.register(MovieTrailer)
admin.site.register(Genre)

